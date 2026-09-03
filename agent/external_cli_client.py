"""Bounded external CLI transport — Claude Code subprocess client.

Invokes ``claude -p`` (non-bare) with explicit structured output and safety
flags, delivers the prompt through stdin, and parses the newline-delimited
JSON (``stream-json`` or ``json``) event stream.

Key safety properties:
  - Never imports anthropic SDK or calls the Anthropic API.
  - Never logs credentials, tokens, or prompt text.
  - Child environment is explicitly sanitized: ANTHROPIC_API_KEY and related
    override variables are removed before launch.
  - Command and args are an explicit list; no shell=True, no string parsing.
  - cwd must resolve under a configured trusted root (validated by the caller).
  - stdout/stderr/stdin are bounded by configurable byte ceilings.
  - Process group is killed on timeout or cancellation.
  - Partial events are never returned as final text.

This module is the wire-level subprocess driver only. Higher-level delegation
integration (cwd validation, credential resolution, concurrency, config) lives
in tools/delegate_tool.py.

Usage (internal / testing only)::

    client = ExternalCLIClient(
        command="claude",
        args=["-p", "", "--output-format", "stream-json", ...],
        cwd="/tmp/project",
        env={"CLAUDE_CODE_OAUTH_TOKEN": "..."},  # child-only
        prompt="explain this code",
        timeout=60.0,
    )
    result = client.run()
    # result.status  -> "completed" | "failed" | "timeout" | "cancelled" | ...
    # result.summary -> terminal result text or None
"""

from __future__ import annotations

import json
import logging
import os
import platform
import queue
import signal
import subprocess
import threading
import time
from dataclasses import dataclass, field
from typing import Any, Callable, Dict, Iterator, List, Optional, Sequence

logger = logging.getLogger(__name__)

_IS_WINDOWS = platform.system() == "Windows"

# ---------------------------------------------------------------------------
# Hard safety ceilings — operator config may be *lower* but not higher.
# ---------------------------------------------------------------------------
_MAX_INPUT_BYTES_CAP = 10 * 1024 * 1024   # 10 MiB (documented Claude Code stdin cap)
_MAX_STDOUT_BYTES_CAP = 8 * 1024 * 1024   # 8 MiB
_MAX_STDERR_BYTES_CAP = 256 * 1024         # 256 KiB
_MAX_TURNS_CAP = 200
_MAX_CONCURRENT_CAP = 8
_MAX_TIMEOUT_SECONDS_CAP = 900.0

# Conservative conservative defaults (task body / architecture contract)
_DEFAULT_INPUT_MAX_BYTES = 10 * 1024 * 1024
_DEFAULT_STDOUT_MAX_BYTES = 8 * 1024 * 1024
_DEFAULT_STDERR_MAX_BYTES = 64 * 1024
_DEFAULT_TIMEOUT_SECONDS = 900.0
_DEFAULT_MAX_TURNS = 20
_DEFAULT_RETRY_LIMIT = 0

# Shutdown grace periods (seconds)
_SIGINT_GRACE = 2.0
_SIGTERM_GRACE = 3.0
_SIGKILL_GRACE = 2.0

# Flags that Hermes controls; reject duplicates from external sources.
_HERMES_OWNED_FLAGS = frozenset([
    "-p", "--print",
    "--bare",
    "--output-format",
    "--verbose",
    "--include-partial-messages",
    "--no-session-persistence",
    "--permission-mode",
    "--allowedTools", "--allowed-tools",
    "--tools",
    "--max-turns",
    "--max-budget-usd",
    "--resume", "--continue",
    "--cloud",
    "--bg", "--background",
    "--dangerously-skip-permissions",
])

# The child must use Claude Code's subscription/OAuth path, never an
# Anthropic API or cloud-provider override.  These keys are rejected when a
# caller tries to add them and stripped from the inherited environment.
_FORBIDDEN_ENV_KEYS = frozenset([
    "ANTHROPIC_API_KEY",
    "ANTHROPIC_AUTH_TOKEN",
    "ANTHROPIC_BASE_URL",
    "ANTHROPIC_BETA",
    "ANTHROPIC_MODEL",
    "CLAUDE_CODE_USE_BEDROCK",
    "CLAUDE_CODE_USE_VERTEX",
    "CLAUDE_CODE_API_KEY_HELPER",
    "CLAUDE_CODE_PROFILE",
    "CLAUDE_CODE_CLOUD",
    "AWS_PROFILE",
    "AWS_REGION",
    "AWS_DEFAULT_REGION",
    "GOOGLE_CLOUD_PROJECT",
    "CLOUD_ML_REGION",
    "VERTEXAI_PROJECT",
    "VERTEXAI_LOCATION",
])
_ALLOWED_EXTRA_ENV_KEYS = frozenset({"CLAUDE_CODE_OAUTH_TOKEN"})

# The external lane is intentionally narrower than the complete Claude Code
# CLI.  These are the only operator flags that do not widen filesystem,
# session, transport, or permission scope.  Hermes owns all protocol and
# budget flags below, so they are rejected separately by _reject_duplicate_flags.
_ALLOWED_EXTRA_FLAGS = frozenset({"--model", "--effort", "--fallback-model"})

# Environment variables to strip before launching the child. Prevents
# API-key precedence overriding CLAUDE_CODE_OAUTH_TOKEN.
_STRIP_ENV_KEYS = frozenset([
    "ANTHROPIC_API_KEY",
    "ANTHROPIC_AUTH_TOKEN",
    "ANTHROPIC_BASE_URL",
    "ANTHROPIC_BETA",
    "ANTHROPIC_MODEL",
])


# ---------------------------------------------------------------------------
# Result dataclasses
# ---------------------------------------------------------------------------

@dataclass
class UsageInfo:
    """Token usage from the terminal result event (may be absent)."""
    input_tokens: int = 0
    output_tokens: int = 0
    reasoning_tokens: Optional[int] = None
    cache_read_tokens: Optional[int] = None
    cache_creation_tokens: Optional[int] = None
    # "reported" | "unavailable" | "unverified"
    source: str = "unavailable"


@dataclass
class CLIResult:
    """Return value of ExternalCLIClient.run()."""
    backend: str = "claude-code-cli"
    # "completed" | "failed" | "timeout" | "cancelled" | "protocol_error"
    # | "auth_unavailable" | "input_too_large" | "output_truncated"
    status: str = "failed"
    summary: Optional[str] = None
    session_id: Optional[str] = None
    model: Optional[str] = None
    exit_reason: Optional[str] = None
    usage: UsageInfo = field(default_factory=UsageInfo)
    cost_usd: Optional[float] = None
    # "reported" | "unavailable" | "unverified"
    cost_status: str = "unavailable"
    num_turns: Optional[int] = None
    duration_seconds: float = 0.0
    malformed_event_count: int = 0
    # Internal: populated when status == "failed" or "protocol_error"
    error_detail: Optional[str] = None


# ---------------------------------------------------------------------------
# Environment sanitization
# ---------------------------------------------------------------------------

def _build_child_env(
    extra_env: Optional[Dict[str, str]] = None,
) -> Dict[str, str]:
    """Build a sanitized child environment.

    Starts from the current process env, strips credential-shadowing keys,
    then overlays ``extra_env`` (which may supply CLAUDE_CODE_OAUTH_TOKEN).
    The token is never echoed in logs.
    """
    env = os.environ.copy()
    for key in _FORBIDDEN_ENV_KEYS:
        env.pop(key, None)
    if extra_env:
        for key, val in extra_env.items():
            if key not in _ALLOWED_EXTRA_ENV_KEYS:
                raise ValueError(
                    f"extra_env may only set {sorted(_ALLOWED_EXTRA_ENV_KEYS)!r}"
                )
            env[key] = val
    return env


# ---------------------------------------------------------------------------
# Argument validation
# ---------------------------------------------------------------------------

def _reject_duplicate_flags(extra_args: Sequence[str]) -> None:
    """Raise ValueError if extra_args contains any Hermes-owned flag.

    This enforces argv precedence: Hermes-generated flags are authoritative;
    no config snippet or task-supplied arg may override them.
    """
    args = [str(arg) for arg in extra_args]
    index = 0
    while index < len(args):
        arg = args[index]
        flag = str(arg).split("=", 1)[0]
        if flag in _HERMES_OWNED_FLAGS:
            raise ValueError(
                f"extra_args must not contain Hermes-controlled flag {arg!r}. "
                "Hermes-generated safety flags take precedence over all args."
            )
        if flag not in _ALLOWED_EXTRA_FLAGS:
            raise ValueError(
                f"extra_args contains unsupported or scope-widening flag {arg!r}. "
                f"Only {sorted(_ALLOWED_EXTRA_FLAGS)!r} may be configured."
            )
        if "=" not in arg:
            if index + 1 >= len(args) or args[index + 1].startswith("-"):
                raise ValueError(f"extra_args flag {arg!r} requires a value")
            index += 2
        else:
            index += 1


# ---------------------------------------------------------------------------
# Stream-JSON / JSON parser
# ---------------------------------------------------------------------------

@dataclass
class _ParsedEvent:
    type: str
    raw: dict
    line: bytes


def _parse_ndjson_line(line: bytes) -> Optional[_ParsedEvent]:
    """Parse one newline-delimited JSON line from the Claude CLI output.

    Returns None for blank lines. Raises ValueError for malformed JSON.
    """
    stripped = line.strip()
    if not stripped:
        return None
    try:
        obj = json.loads(stripped)
    except json.JSONDecodeError as exc:
        raise ValueError(f"malformed JSON: {exc}") from exc
    if not isinstance(obj, dict):
        raise ValueError(f"expected JSON object, got {type(obj).__name__}")
    event_type = obj.get("type", "")
    return _ParsedEvent(type=str(event_type), raw=obj, line=stripped)


class StreamParser:
    """Stateful parser for the Claude CLI ``stream-json`` event stream.

    Invariants:
      - Only a terminal ``type: "result"`` event sets self.result.
      - Partial ``assistant`` and ``text`` events accumulate partial_text
        but never set result.
      - Malformed lines are counted; the caller decides whether to abort.
      - The parser raises no exceptions itself; callers handle them.
    """

    def __init__(self, event_callback: Optional[Callable[[dict], None]] = None) -> None:
        self.result: Optional[dict] = None
        self.model: Optional[str] = None
        self.session_id: Optional[str] = None
        self.partial_texts: List[str] = []
        self.tool_events: List[dict] = []
        self.system_events: List[dict] = []
        self.retry_events: List[dict] = []
        self.malformed: int = 0
        self._stdout_bytes: int = 0
        self._event_callback = event_callback
        self._event_sequence = 0

    def _emit_event(self, event_type: str, raw: dict) -> None:
        """Emit bounded metadata, never raw prompt/result/tool payloads."""
        if self._event_callback is None:
            return
        event_name = {
            "system": "system_init",
            "assistant": "partial",
            "text": "partial",
            "content_block_delta": "partial",
            "tool_use": "tool_use",
            "api_error": "api_retry",
            "api_retry": "api_retry",
            "result": "result",
        }.get(event_type)
        if event_name is None:
            return
        self._event_sequence += 1
        event: Dict[str, Any] = {
            "schema_version": 1,
            "type": "delegation_event",
            "event": event_name,
            "seq": self._event_sequence,
        }
        for key in ("model", "session_id"):
            value = raw.get(key)
            if isinstance(value, str) and value:
                event[key] = value
        if event_name == "tool_use":
            tool_name = raw.get("name") or raw.get("tool_name")
            if isinstance(tool_name, str) and tool_name:
                event["tool_name"] = tool_name[:128]
        elif event_name == "api_retry":
            for key in ("attempt", "max_retries"):
                value = raw.get(key)
                if isinstance(value, int):
                    event[key] = value
        elif event_name == "result":
            subtype = raw.get("subtype")
            if isinstance(subtype, str):
                event["status"] = subtype[:64]
        try:
            self._event_callback(event)
        except Exception:
            logger.debug("external_cli_client: event callback failed", exc_info=True)

    def feed(self, line: bytes, stdout_cap: int) -> Optional[str]:
        """Feed one raw line.

        Returns a control string if the caller should act:
          "result"   — terminal result event received, stop reading
          "truncate" — stdout_cap exceeded before result, stop reading
          None       — continue

        Never raises; records malformed lines internally.
        """
        self._stdout_bytes += len(line)
        if self._stdout_bytes > stdout_cap:
            return "truncate"
        try:
            evt = _parse_ndjson_line(line)
        except ValueError:
            self.malformed += 1
            logger.debug("external_cli_client: malformed line (ignored)")
            return None
        if evt is None:
            return None  # blank line

        etype = evt.type
        raw = evt.raw
        # Claude Code's stream-json protocol wraps Anthropic streaming events
        # inside {"type":"stream_event", "event":{...}}. Normalize that
        # envelope while retaining only the bounded fields used below. Older
        # Claude versions also emit content_block_start for tool use, which is
        # promoted to the same internal tool event as the flatter protocol.
        if etype == "stream_event" and isinstance(raw.get("event"), dict):
            outer = raw
            nested = dict(raw["event"])
            for key in ("model", "session_id"):
                if key in outer and key not in nested:
                    nested[key] = outer[key]
            etype = str(nested.get("type", ""))
            raw = nested
            if etype == "content_block_start":
                block = raw.get("content_block")
                if isinstance(block, dict) and block.get("type") == "tool_use":
                    tool_event = dict(raw)
                    tool_event["name"] = block.get("name", "")
                    raw = tool_event
                    etype = "tool_use"
        self._emit_event(etype, raw)

        if etype == "system":
            self.system_events.append(raw)
            self.model = raw.get("model") or self.model
            self.session_id = raw.get("session_id") or self.session_id

        elif etype == "result":
            # Terminal event — capture and signal the caller to stop.
            self.result = raw
            self.model = raw.get("model") or self.model
            self.session_id = raw.get("session_id") or self.session_id
            return "result"

        elif etype == "assistant":
            # Partial assistant message — accumulate but never finalise.
            message = raw.get("message") or {}
            for block in (message.get("content") or []):
                if isinstance(block, dict) and block.get("type") == "text":
                    text = block.get("text", "")
                    if text:
                        self.partial_texts.append(text)

        elif etype in ("text", "content_block_delta"):
            # Stream-json partial deltas
            delta = raw.get("delta") or raw
            text = delta.get("text", "")
            if text:
                self.partial_texts.append(str(text))

        elif etype == "tool_use":
            self.tool_events.append(raw)

        elif etype in ("api_error", "api_retry"):
            self.retry_events.append(raw)

        return None

    def finalise(self, exit_code: Optional[int]) -> CLIResult:
        """Convert accumulated parser state into a CLIResult.

        Must only be called once, after the process has exited or been killed.
        """
        result = CLIResult()
        result.model = self.model
        result.session_id = self.session_id
        result.malformed_event_count = self.malformed

        if self.result is not None:
            r = self.result
            subtype = r.get("subtype", "")
            result.exit_reason = subtype or "unknown"

            # Terminal summary: only from the "result" event.
            result.summary = r.get("result") or r.get("text") or None

            # Usage — report verbatim if present, mark unverified (estimated).
            usage_raw = r.get("usage") or {}
            if isinstance(usage_raw, dict) and usage_raw:
                def _counter(key: str, default: Optional[int] = 0) -> Optional[int]:
                    value = usage_raw.get(key, default)
                    if value is None and default is None:
                        return None
                    if isinstance(value, bool):
                        return None
                    try:
                        parsed = int(str(value))
                    except (TypeError, ValueError, OverflowError):
                        return None
                    return parsed if parsed >= 0 else None

                input_tokens = _counter("input_tokens")
                output_tokens = _counter("output_tokens")
                thinking_tokens = _counter("thinking_tokens", None)
                cache_read_tokens = _counter("cache_read_input_tokens", None)
                cache_creation_tokens = _counter("cache_creation_input_tokens", None)
                if input_tokens is not None and output_tokens is not None:
                    result.usage = UsageInfo(
                        input_tokens=input_tokens,
                        output_tokens=output_tokens,
                        reasoning_tokens=thinking_tokens,
                        cache_read_tokens=cache_read_tokens,
                        cache_creation_tokens=cache_creation_tokens,
                        source="unverified",  # client-side estimate, not billing truth
                    )

            # Cost — mark as unverified if present.
            cost = r.get("total_cost_usd") or r.get("cost_usd")
            if cost is not None:
                try:
                    result.cost_usd = float(cost)
                    result.cost_status = "unverified"
                except (TypeError, ValueError):
                    pass

            result.num_turns = r.get("num_turns")

            if subtype == "success" and exit_code not in (None, 0):
                result.status = "failed"
                result.error_detail = (
                    f"Terminal success event accompanied by exit_code={exit_code}"
                )
            elif subtype == "success":
                result.status = "completed"
            elif subtype in ("error_max_turns", "error_max_budget_usd"):
                result.status = "failed"
            elif subtype:
                result.status = "failed"
            else:
                result.status = "completed"

        elif exit_code is not None and exit_code == 0 and not self.result:
            # Process exited cleanly but no result event — protocol error.
            result.status = "protocol_error"
            result.error_detail = "Process exited 0 but emitted no terminal result event"
        else:
            result.status = "protocol_error"
            result.error_detail = (
                f"No terminal result event received (exit_code={exit_code})"
            )

        return result


# ---------------------------------------------------------------------------
# Process-group termination helpers
# ---------------------------------------------------------------------------

def _terminate_process_group(proc: subprocess.Popen, reason: str) -> None:
    """Shut down the process group using escalating signals.

    Sequence (POSIX):
      1. Close stdin (graceful turn termination).
      2. SIGINT to process group — wait _SIGINT_GRACE s.
      3. SIGTERM to process group — wait _SIGTERM_GRACE s.
      4. SIGKILL to process group — wait _SIGKILL_GRACE s.
      5. Reap with proc.wait(timeout=1).

    On Windows: proc.terminate() + proc.wait(), no process-group semantics.
    """
    logger.debug("external_cli_client: terminating child process-group (%s)", reason)

    # 1. Close stdin
    try:
        if proc.stdin and not proc.stdin.closed:
            proc.stdin.close()
    except Exception:
        pass

    if _IS_WINDOWS:
        try:
            proc.terminate()
        except Exception:
            pass
        try:
            proc.wait(timeout=_SIGTERM_GRACE + _SIGKILL_GRACE)
        except subprocess.TimeoutExpired:
            try:
                proc.kill()
                proc.wait(timeout=_SIGKILL_GRACE)
            except Exception:
                pass
        return

    # POSIX: send to the whole process group via os.killpg
    try:
        pgid = os.getpgid(proc.pid)
    except (ProcessLookupError, PermissionError):
        pgid = None

    def _kill_group(sig: signal.Signals) -> None:  # type: ignore[name-defined]
        if pgid is None:
            return
        try:
            os.killpg(pgid, sig)  # windows-footgun: ok — inside _IS_WINDOWS guard
        except (ProcessLookupError, PermissionError):
            pass

    _kill_group(signal.SIGINT)
    deadline = time.monotonic() + _SIGINT_GRACE
    while time.monotonic() < deadline:
        if proc.poll() is not None:
            break
        time.sleep(0.05)

    if proc.poll() is None:
        _kill_group(signal.SIGTERM)
        deadline = time.monotonic() + _SIGTERM_GRACE
        while time.monotonic() < deadline:
            if proc.poll() is not None:
                break
            time.sleep(0.05)

    if proc.poll() is None:
        _kill_group(signal.SIGKILL)
        try:
            proc.wait(timeout=_SIGKILL_GRACE)
        except subprocess.TimeoutExpired:
            pass

    # Final reap to avoid zombie
    try:
        proc.wait(timeout=1.0)
    except (subprocess.TimeoutExpired, ChildProcessError):
        pass


# ---------------------------------------------------------------------------
# Stderr reader thread
# ---------------------------------------------------------------------------

class _StderrReader(threading.Thread):
    """Drains stderr in a background thread; bounded by stderr_cap bytes."""

    def __init__(self, pipe, cap: int) -> None:
        super().__init__(daemon=True)
        self._pipe = pipe
        self._cap = cap
        self._lines: List[bytes] = []
        self._bytes: int = 0
        self._truncated: bool = False

    def run(self) -> None:
        try:
            for line in iter(self._pipe.readline, b""):
                remaining = self._cap - self._bytes
                if remaining <= 0:
                    self._truncated = True
                    continue
                chunk = line[:remaining]
                if chunk:
                    self._lines.append(chunk)
                    self._bytes += len(chunk)
                if len(line) > remaining:
                    self._truncated = True
        except Exception:
            pass
        finally:
            try:
                self._pipe.close()
            except Exception:
                pass

    def tail(self, n: int = 20) -> List[str]:
        """Return last n lines as decoded strings (safe for diagnostics)."""
        return [
            ln.decode("utf-8", errors="replace").rstrip()
            for ln in self._lines[-n:]
        ]

    @property
    def truncated(self) -> bool:
        return self._truncated


# ---------------------------------------------------------------------------
# Main client
# ---------------------------------------------------------------------------

class ExternalCLIClient:
    """Bounded subprocess wrapper for ``claude -p``.

    This class is NOT thread-safe — one caller drives it at a time.

    Parameters
    ----------
    command:
        Path or name of the ``claude`` executable.
    args:
        Additional flags appended AFTER the Hermes-mandatory set. Must not
        include any flag in _HERMES_OWNED_FLAGS (validated at construction).
    cwd:
        Trusted working directory for the child process. The caller is
        responsible for validating that cwd resolves under a configured
        trusted root.
    env:
        Child-only environment additions (e.g. ``CLAUDE_CODE_OAUTH_TOKEN``).
        Merged with the sanitized parent env; ANTHROPIC_API_KEY is stripped.
    prompt:
        The user-facing task text. Delivered via stdin, NOT argv. Must not
        exceed input_max_bytes.
    output_format:
        ``"stream-json"`` (default) or ``"json"`` (final only, compatibility).
    permission_mode:
        Claude CLI permission-mode flag value. Default ``"dontAsk"``.
    allowed_tools:
        Explicit tool allowlist passed via ``--allowedTools``.
    max_turns:
        ``--max-turns`` value; capped at _MAX_TURNS_CAP.
    max_budget_usd:
        ``--max-budget-usd`` float or None.
    timeout:
        Wall-clock deadline in seconds; must be positive.
    input_max_bytes:
        Prompt size ceiling; capped at _MAX_INPUT_BYTES_CAP.
    stdout_max_bytes:
        Stdout byte ceiling; capped at _MAX_STDOUT_BYTES_CAP.
    stderr_max_bytes:
        Stderr byte ceiling; capped at _MAX_STDERR_BYTES_CAP.
    cancel_event:
        Optional threading.Event; when set, the run() loop terminates the
        child and returns status="cancelled".
    event_callback:
        Optional callback receiving versioned, credential-free lifecycle and
        stream metadata events as they arrive.
    """

    def __init__(
        self,
        *,
        command: str = "claude",
        args: Sequence[str] = (),
        cwd: str,
        env: Optional[Dict[str, str]] = None,
        prompt: str,
        output_format: str = "stream-json",
        permission_mode: str = "dontAsk",
        allowed_tools: Sequence[str] = (),
        max_turns: int = _DEFAULT_MAX_TURNS,
        max_budget_usd: Optional[float] = None,
        timeout: float = _DEFAULT_TIMEOUT_SECONDS,
        input_max_bytes: int = _DEFAULT_INPUT_MAX_BYTES,
        stdout_max_bytes: int = _DEFAULT_STDOUT_MAX_BYTES,
        stderr_max_bytes: int = _DEFAULT_STDERR_MAX_BYTES,
        cancel_event: Optional[threading.Event] = None,
        event_callback: Optional[Callable[[dict], None]] = None,
    ) -> None:
        if not command:
            raise ValueError("command must not be empty")
        if not cwd:
            raise ValueError("cwd must be provided")

        # Validate extra args don't contain Hermes-owned flags
        _reject_duplicate_flags(args)

        # Clamp configurable limits to hard ceilings
        if int(max_turns) <= 0:
            raise ValueError("max_turns must be positive")
        if float(timeout) <= 0:
            raise ValueError("timeout must be positive")
        if int(input_max_bytes) <= 0 or int(stdout_max_bytes) <= 0 or int(stderr_max_bytes) <= 0:
            raise ValueError("input and output byte limits must be positive")
        if max_budget_usd is not None and float(max_budget_usd) < 0:
            raise ValueError("max_budget_usd must not be negative")
        if output_format not in {"stream-json", "json"}:
            raise ValueError("output_format must be 'stream-json' or 'json'")
        if permission_mode not in {"dontAsk", "default"}:
            raise ValueError("permission_mode must be 'dontAsk' or 'default'")
        self._max_turns = min(int(max_turns), _MAX_TURNS_CAP)
        self._timeout = min(float(timeout), _MAX_TIMEOUT_SECONDS_CAP)
        self._input_max_bytes = min(int(input_max_bytes), _MAX_INPUT_BYTES_CAP)
        self._stdout_max_bytes = min(int(stdout_max_bytes), _MAX_STDOUT_BYTES_CAP)
        self._stderr_max_bytes = min(int(stderr_max_bytes), _MAX_STDERR_BYTES_CAP)

        self._command = command
        self._extra_args = list(args)
        self._cwd = cwd
        self._env = _build_child_env(env)
        self._prompt = prompt
        self._output_format = output_format
        self._permission_mode = permission_mode
        self._allowed_tools = list(allowed_tools)
        self._max_budget_usd = max_budget_usd
        self._cancel_event = cancel_event
        self._event_callback = event_callback
        self._event_sequence = 0

    def _emit_lifecycle_event(self, event_name: str, **fields: Any) -> None:
        if self._event_callback is None:
            return
        self._event_sequence += 1
        event: Dict[str, Any] = {
            "schema_version": 1,
            "type": "delegation_event",
            "event": event_name,
            "seq": self._event_sequence,
        }
        event.update(fields)
        try:
            self._event_callback(event)
        except Exception:
            logger.debug("external_cli_client: lifecycle callback failed", exc_info=True)

    def _forward_stream_event(self, event: dict) -> None:
        """Forward parser metadata with one sequence shared by all events."""
        if self._event_callback is None:
            return
        forwarded = dict(event)
        self._event_sequence += 1
        forwarded["seq"] = self._event_sequence
        try:
            self._event_callback(forwarded)
        except Exception:
            logger.debug("external_cli_client: stream callback failed", exc_info=True)

    def _build_argv(self) -> List[str]:
        """Construct the full argv list.

        Hermes-mandatory flags come first, then operator extra_args.
        The prompt placeholder in -p is empty (""); the real content arrives
        through stdin, which keeps user data out of argv and process listings.
        """
        argv: List[str] = [self._command, "-p", ""]
        argv += ["--output-format", self._output_format]
        argv += ["--verbose"]
        argv += ["--include-partial-messages"]
        argv += ["--no-session-persistence"]
        argv += ["--permission-mode", self._permission_mode]
        if self._allowed_tools:
            argv += ["--allowedTools"] + self._allowed_tools
        argv += ["--max-turns", str(self._max_turns)]
        if self._max_budget_usd is not None:
            argv += ["--max-budget-usd", f"{self._max_budget_usd:.2f}"]
        # Operator-supplied extra args (already validated)
        argv += self._extra_args
        return argv

    def run(self) -> CLIResult:
        """Invoke the CLI, parse output, and return a CLIResult.

        This call blocks until the process exits, the deadline fires, or the
        cancel_event is set. The process group is always reaped before return.
        """
        prompt_bytes = self._prompt.encode("utf-8", errors="replace")
        if len(prompt_bytes) > self._input_max_bytes:
            r = CLIResult()
            r.status = "input_too_large"
            r.error_detail = (
                f"Prompt is {len(prompt_bytes)} bytes, exceeds limit {self._input_max_bytes}"
            )
            return r

        argv = self._build_argv()
        start = time.monotonic()

        popen_kwargs: Dict[str, Any] = dict(
            args=argv,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            cwd=self._cwd,
            env=self._env,
            bufsize=0,
        )
        if not _IS_WINDOWS:
            popen_kwargs["start_new_session"] = True  # new session → new process group

        try:
            proc = subprocess.Popen(**popen_kwargs)
        except (FileNotFoundError, PermissionError, OSError) as exc:
            r = CLIResult()
            r.status = "failed"
            r.error_detail = f"Failed to launch {self._command!r}: {exc}"
            r.duration_seconds = time.monotonic() - start
            return r

        self._emit_lifecycle_event("process_started")

        logger.debug(
            "external_cli_client: launched pid=%d command=%r cwd=%r",
            proc.pid, argv[0], self._cwd,
        )

        # Start stderr reader thread
        stderr_reader = _StderrReader(proc.stderr, self._stderr_max_bytes)
        stderr_reader.start()

        parser = StreamParser(event_callback=self._forward_stream_event)
        status_override: Optional[str] = None
        cancelled = False

        # ``readline()`` on a pipe cannot be interrupted by a wall-clock
        # deadline.  A daemon reader thread lets the control loop poll for
        # output and cancellation without waiting on a silent child (or a
        # descendant that inherited stdout).
        stdout_queue: "queue.Queue[Optional[bytes]]" = queue.Queue()

        def _read_stdout() -> None:
            try:
                for stdout_line in iter(proc.stdout.readline, b""):
                    stdout_queue.put(stdout_line)
            except Exception:
                pass
            finally:
                stdout_queue.put(None)

        stdout_reader = threading.Thread(target=_read_stdout, daemon=True)
        stdout_reader.start()

        try:
            # Deliver prompt via stdin then close it
            try:
                proc.stdin.write(prompt_bytes)
                proc.stdin.close()
            except BrokenPipeError:
                # Process died before we finished writing
                pass
            except Exception as exc:
                logger.debug("external_cli_client: stdin write error: %s", exc)

            # Read stdout line by line with deadline.  The queue timeout is
            # deliberately short so cancellation is observed promptly.
            deadline = start + self._timeout
            while True:
                remaining = deadline - time.monotonic()
                if remaining <= 0:
                    status_override = "timeout"
                    break
                if self._cancel_event and self._cancel_event.is_set():
                    cancelled = True
                    break
                try:
                    line = stdout_queue.get(timeout=min(remaining, 0.1))
                except queue.Empty:
                    continue
                if line is None:
                    break
                ctrl = parser.feed(line, self._stdout_max_bytes)
                if ctrl == "result":
                    break
                if ctrl == "truncate":
                    status_override = "output_truncated"
                    break

            # Check cancellation / deadline again after loop exits (e.g. if
            # readline blocked and returned an empty byte string after a slow
            # response, making the for-loop end naturally instead of via break).
            if self._cancel_event and self._cancel_event.is_set():
                cancelled = True
            elif status_override is None and time.monotonic() >= deadline:
                status_override = "timeout"

        finally:
            # Determine reason and kill process group
            if cancelled:
                _terminate_process_group(proc, "cancelled")
            elif status_override == "timeout":
                _terminate_process_group(proc, "timeout")
            else:
                # Normal exit: give a brief grace for drain, then reap
                try:
                    proc.wait(timeout=5.0)
                except subprocess.TimeoutExpired:
                    _terminate_process_group(proc, "drain_timeout")
                try:
                    proc.stdout.close()
                except Exception:
                    pass

        exit_code = proc.returncode
        duration = time.monotonic() - start
        stdout_reader.join(timeout=2.0)
        stderr_reader.join(timeout=2.0)

        # Assemble result
        result = parser.finalise(exit_code)
        result.duration_seconds = duration

        # Apply overrides from loop
        if cancelled:
            result.status = "cancelled"
            result.error_detail = "Cancelled by caller"
            self._emit_lifecycle_event("cancelled", status="cancelled")
        elif status_override == "timeout":
            result.status = "timeout"
            result.error_detail = (
                f"Deadline exceeded after {self._timeout:.1f}s"
            )
            self._emit_lifecycle_event("timeout", status="timeout")
        elif status_override == "output_truncated":
            result.status = "output_truncated"
            result.error_detail = (
                f"stdout exceeded {self._stdout_max_bytes} bytes"
            )

        self._emit_lifecycle_event(
            "process_exit",
            status=result.status,
            exit_code=exit_code,
        )

        logger.debug(
            "external_cli_client: done status=%s exit_code=%s duration=%.1fs",
            result.status, exit_code, duration,
        )
        return result


# ---------------------------------------------------------------------------
# Concurrency guard
# ---------------------------------------------------------------------------

class ConcurrencyLimitError(RuntimeError):
    """Raised when max_concurrent running clients would be exceeded."""


class ConcurrentExternalCLIRunner:
    """Semaphore-bounded wrapper for running ExternalCLIClient instances.

    Instantiate once and call run_bounded(); excess calls raise
    ConcurrencyLimitError immediately (fail-fast, no queue).

    Parameters
    ----------
    max_concurrent:
        Maximum number of simultaneous CLI invocations; capped at
        _MAX_CONCURRENT_CAP.
    """

    def __init__(self, max_concurrent: int = 1) -> None:
        requested = int(max_concurrent)
        if requested <= 0:
            raise ValueError("max_concurrent must be positive")
        self._max = min(requested, _MAX_CONCURRENT_CAP)
        self._sem = threading.Semaphore(self._max)
        self._lock = threading.Lock()
        self._active = 0

    @property
    def active(self) -> int:
        with self._lock:
            return self._active

    def run_bounded(self, client: ExternalCLIClient) -> CLIResult:
        """Acquire the semaphore and run the client; raise if at capacity."""
        acquired = self._sem.acquire(blocking=False)
        if not acquired:
            raise ConcurrencyLimitError(
                f"At max_concurrent={self._max} concurrent CLI invocations"
            )
        with self._lock:
            self._active += 1
        try:
            return client.run()
        finally:
            with self._lock:
                self._active -= 1
            self._sem.release()
