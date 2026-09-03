import ast
import io
import json
import os
import stat
import threading
import time

import pytest

from agent.external_cli_client import (
    CLIResult,
    ConcurrentExternalCLIRunner,
    ConcurrencyLimitError,
    ExternalCLIClient,
    _StderrReader,
    _build_child_env,
    _reject_duplicate_flags,
)


def _fake_cli(tmp_path, body):
    path = tmp_path / "fake-claude"
    path.write_text("#!/bin/sh\n" + body)
    path.chmod(path.stat().st_mode | stat.S_IXUSR)
    return str(path)


def test_rejects_owned_flags_with_equals_form():
    with pytest.raises(ValueError):
        _reject_duplicate_flags(["--max-turns=999"])


def test_rejects_external_args_that_escape_project_scope():
    with pytest.raises(ValueError):
        ExternalCLIClient(
            command="claude",
            cwd="/tmp",
            prompt="hello",
            args=["--add-dir", "/outside"],
        )


def test_child_environment_clears_api_shadowing_and_rejects_overrides(monkeypatch):
    monkeypatch.setenv("ANTHROPIC_API_KEY", "must-not-leak")
    monkeypatch.setenv("ANTHROPIC_AUTH_TOKEN", "must-not-leak")
    env = _build_child_env({"CLAUDE_CODE_OAUTH_TOKEN": "oauth-token"})
    assert "ANTHROPIC_API_KEY" not in env
    assert "ANTHROPIC_AUTH_TOKEN" not in env
    assert env["CLAUDE_CODE_OAUTH_TOKEN"] == "oauth-token"

    with pytest.raises(ValueError):
        _build_child_env({"ANTHROPIC_API_KEY": "shadow"})


def test_stderr_reader_never_retains_bytes_above_cap():
    reader = _StderrReader(io.BytesIO(b"0123456789abcdef\n"), cap=10)
    reader.run()
    assert reader._bytes == 10
    assert reader.truncated is True
    assert len("".join(reader.tail()).encode()) <= 10


def test_stream_result_uses_terminal_event_only(tmp_path):
    command = _fake_cli(
        tmp_path,
        """cat >/dev/null
printf '%s\\n' '{\"type\":\"system\",\"model\":\"claude-test\"}'
printf '%s\\n' '{\"type\":\"assistant\",\"message\":{\"content\":[{\"type\":\"text\",\"text\":\"partial\"}]}}'
printf '%s\\n' '{\"type\":\"result\",\"subtype\":\"success\",\"result\":\"final\",\"session_id\":\"s1\"}'
""",
    )
    result = ExternalCLIClient(
        command=command,
        cwd=str(tmp_path),
        prompt="hello",
        timeout=5,
    ).run()
    assert result.status == "completed"
    assert result.summary == "final"
    assert result.session_id == "s1"
    assert result.model == "claude-test"


def test_streams_sanitized_structured_events(tmp_path):
    command = _fake_cli(
        tmp_path,
        """cat >/dev/null
printf '%s\\n' '{\"type\":\"system\",\"model\":\"claude-test\",\"session_id\":\"s1\"}'
printf '%s\\n' '{\"type\":\"assistant\",\"message\":{\"content\":[{\"type\":\"text\",\"text\":\"secret partial\"}]}}'
printf '%s\\n' '{\"type\":\"tool_use\",\"name\":\"Read\",\"input\":{\"path\":\"secret.txt\"}}'
printf '%s\\n' '{\"type\":\"api_retry\",\"attempt\":1,\"max_retries\":2,\"error\":\"token should not escape\"}'
printf '%s\\n' '{\"type\":\"result\",\"subtype\":\"success\",\"result\":\"final\",\"session_id\":\"s1\"}'
""",
    )
    events = []
    result = ExternalCLIClient(
        command=command,
        cwd=str(tmp_path),
        prompt="hello",
        timeout=5,
        event_callback=events.append,
    ).run()

    assert result.status == "completed"
    assert [event["event"] for event in events] == [
        "process_started",
        "system_init",
        "partial",
        "tool_use",
        "api_retry",
        "result",
        "process_exit",
    ]
    assert all("secret" not in str(event) for event in events)


def test_parses_nested_claude_stream_events_without_using_partial_as_final(tmp_path):
    command = _fake_cli(
        tmp_path,
        """cat >/dev/null
printf '%s\\n' '{\"type\":\"system\",\"model\":\"claude-test\"}'
printf '%s\\n' '{\"type\":\"stream_event\",\"event\":{\"type\":\"content_block_delta\",\"delta\":{\"type\":\"text_delta\",\"text\":\"partial\"}}}'
printf '%s\\n' '{\"type\":\"stream_event\",\"event\":{\"type\":\"content_block_start\",\"content_block\":{\"type\":\"tool_use\",\"name\":\"Read\"}}}'
printf '%s\\n' '{\"type\":\"result\",\"subtype\":\"success\",\"result\":\"final\"}'
""",
    )
    events = []
    result = ExternalCLIClient(
        command=command,
        cwd=str(tmp_path),
        prompt="hello",
        timeout=5,
        event_callback=events.append,
    ).run()
    assert result.status == "completed"
    assert result.summary == "final"
    assert [event["event"] for event in events] == [
        "process_started", "system_init", "partial", "tool_use", "result", "process_exit"
    ]


def test_malformed_usage_does_not_crash_terminal_result_parsing(tmp_path):
    command = _fake_cli(
        tmp_path,
        """cat >/dev/null
printf '%s\\n' '{\"type\":\"result\",\"subtype\":\"success\",\"result\":\"done\",\"usage\":{\"input_tokens\":\"not-a-number\"}}'
""",
    )
    result = ExternalCLIClient(
        command=command,
        cwd=str(tmp_path),
        prompt="hello",
        timeout=5,
    ).run()
    assert result.status == "completed"
    assert result.summary == "done"
    assert result.usage.source == "unavailable"


def test_malformed_stream_lines_are_counted_but_terminal_result_wins(tmp_path):
    command = _fake_cli(
        tmp_path,
        """cat >/dev/null
printf '%s\\n' 'not-json-at-all'
printf '%s\\n' '{\"type\":\"result\",\"subtype\":\"success\",\"result\":\"done\"}'
""",
    )
    result = ExternalCLIClient(
        command=command,
        cwd=str(tmp_path),
        prompt="hello",
        timeout=5,
    ).run()
    assert result.status == "completed"
    assert result.summary == "done"
    assert result.malformed_event_count == 1


def test_terminal_error_subtype_is_failed_and_retry_is_not_replayed(tmp_path):
    command = _fake_cli(
        tmp_path,
        """cat >/dev/null
printf '%s\\n' '{\"type\":\"api_retry\",\"attempt\":1,\"max_retries\":0}'
printf '%s\\n' '{\"type\":\"result\",\"subtype\":\"error_max_turns\",\"result\":\"turn limit\"}'
""",
    )
    events = []
    result = ExternalCLIClient(
        command=command,
        cwd=str(tmp_path),
        prompt="hello",
        timeout=5,
        event_callback=events.append,
    ).run()
    assert result.status == "failed"
    assert result.summary == "turn limit"
    assert [event["event"] for event in events].count("api_retry") == 1
    assert result.exit_reason == "error_max_turns"


def test_nonzero_process_cannot_claim_success(tmp_path):
    command = _fake_cli(
        tmp_path,
        """cat >/dev/null
printf '%s\\n' '{\"type\":\"result\",\"subtype\":\"success\",\"result\":\"not trusted\"}'
exit 7
""",
    )
    result = ExternalCLIClient(
        command=command,
        cwd=str(tmp_path),
        prompt="hello",
        timeout=5,
    ).run()
    assert result.status == "failed"
    assert "exit_code=7" in (result.error_detail or "")


def test_build_argv_keeps_prompt_out_of_process_arguments():
    client = ExternalCLIClient(
        command="claude",
        cwd="/tmp",
        prompt="sensitive prompt",
        args=["--model", "haiku"],
    )
    argv = client._build_argv()
    assert "sensitive prompt" not in argv
    assert "--bare" not in argv
    assert "--model" in argv


def test_fake_cli_contract_has_exact_mandatory_argv_and_stdin_only_prompt(tmp_path):
    argv_file = tmp_path / "argv.json"
    stdin_file = tmp_path / "stdin.txt"
    command = tmp_path / "fake-claude.py"
    command.write_text(
        "#!/usr/bin/env python3\n"
        "import json, pathlib, sys\n"
        f"pathlib.Path({str(argv_file)!r}).write_text(json.dumps(sys.argv[1:]))\n"
        f"pathlib.Path({str(stdin_file)!r}).write_text(sys.stdin.read())\n"
        "print(json.dumps({'type': 'result', 'subtype': 'success', 'result': 'done'}))\n"
    )
    command.chmod(command.stat().st_mode | stat.S_IXUSR)
    prompt = "prompt must only be sent through stdin"
    result = ExternalCLIClient(
        command=str(command),
        cwd=str(tmp_path),
        prompt=prompt,
        output_format="stream-json",
        permission_mode="dontAsk",
        allowed_tools=["Read", "Grep"],
        max_turns=7,
        max_budget_usd=1.25,
        args=["--model", "haiku"],
        timeout=5,
    ).run()

    assert result.status == "completed"
    assert json.loads(argv_file.read_text()) == [
        "-p", "",
        "--output-format", "stream-json",
        "--verbose",
        "--include-partial-messages",
        "--no-session-persistence",
        "--permission-mode", "dontAsk",
        "--allowedTools", "Read", "Grep",
        "--max-turns", "7",
        "--max-budget-usd", "1.25",
        "--model", "haiku",
    ]
    assert stdin_file.read_text() == prompt
    assert prompt not in argv_file.read_text()


def test_clean_exit_without_terminal_result_is_protocol_error(tmp_path):
    command = _fake_cli(tmp_path, "cat >/dev/null\nprintf '%s\\n' '{\"type\":\"assistant\"}'\n")
    result = ExternalCLIClient(
        command=command,
        cwd=str(tmp_path),
        prompt="hello",
        timeout=5,
    ).run()
    assert result.status == "protocol_error"
    assert result.summary is None
    assert "no terminal result" in (result.error_detail or "").lower()


def test_timeout_does_not_wait_for_silent_child(tmp_path):
    command = _fake_cli(tmp_path, "sleep 2\n")
    started = time.monotonic()
    result = ExternalCLIClient(
        command=command,
        cwd=str(tmp_path),
        prompt="hello",
        timeout=0.2,
    ).run()
    elapsed = time.monotonic() - started
    assert result.status == "timeout"
    assert elapsed < 1.5


def test_json_output_and_usage_cost_metadata_are_preserved(tmp_path):
    command = _fake_cli(
        tmp_path,
        """cat >/dev/null
printf '%s\\n' '{\"type\":\"result\",\"subtype\":\"success\",\"result\":\"json final\",\"model\":\"haiku\",\"session_id\":\"json-s1\",\"num_turns\":3,\"usage\":{\"input_tokens\":12,\"output_tokens\":7,\"thinking_tokens\":2,\"cache_read_input_tokens\":4},\"total_cost_usd\":0.0123}'
""",
    )
    result = ExternalCLIClient(
        command=command,
        cwd=str(tmp_path),
        prompt="hello",
        output_format="json",
        timeout=5,
    ).run()
    assert result.status == "completed"
    assert result.summary == "json final"
    assert result.model == "haiku"
    assert result.session_id == "json-s1"
    assert result.num_turns == 3
    assert result.usage.input_tokens == 12
    assert result.usage.output_tokens == 7
    assert result.usage.reasoning_tokens == 2
    assert result.usage.cache_read_tokens == 4
    assert result.usage.source == "unverified"
    assert result.cost_usd == pytest.approx(0.0123)
    assert result.cost_status == "unverified"


def test_fake_cli_receives_prompt_args_cwd_and_sanitized_child_environment(tmp_path, monkeypatch):
    marker = tmp_path / "child-marker"
    command = _fake_cli(
        tmp_path,
        f"""printf '%s\\n' \"$PWD\" > {marker}.cwd
printf '%s\\n' \"$CLAUDE_CODE_OAUTH_TOKEN\" > {marker}.oauth
printf '%s\\n' \"$ANTHROPIC_API_KEY\" > {marker}.api
printf '%s\\n' \"$@\" > {marker}.args
cat > {marker}.prompt
printf '%s\\n' '{{\"type\":\"result\",\"subtype\":\"success\",\"result\":\"ok\"}}'
""",
    )
    monkeypatch.setenv("ANTHROPIC_API_KEY", "fake-api-secret")
    result = ExternalCLIClient(
        command=command,
        args=["--model", "haiku"],
        cwd=str(tmp_path),
        env={"CLAUDE_CODE_OAUTH_TOKEN": "fake-oauth-secret"},
        prompt="prompt only on stdin",
        timeout=5,
    ).run()
    assert result.status == "completed"
    assert marker.with_suffix(".cwd").read_text().strip() == str(tmp_path)
    assert marker.with_suffix(".oauth").read_text().strip() == "fake-oauth-secret"
    assert marker.with_suffix(".api").read_text().strip() == ""
    assert marker.with_suffix(".prompt").read_text() == "prompt only on stdin"
    args = marker.with_suffix(".args").read_text()
    assert "fake-oauth-secret" not in args
    assert "prompt only on stdin" not in args
    assert "--model" in args
    assert "haiku" in args


def test_prompt_size_guard_prevents_launch(tmp_path):
    command = _fake_cli(tmp_path, "printf 'launched' > launched\n")
    result = ExternalCLIClient(
        command=command,
        cwd=str(tmp_path),
        prompt="é" * 20,
        input_max_bytes=10,
    ).run()
    assert result.status == "input_too_large"
    assert not (tmp_path / "launched").exists()


def test_stdout_cap_is_reported_without_treating_partial_as_final(tmp_path):
    command = _fake_cli(
        tmp_path,
        """cat >/dev/null
printf 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx\\n'
""",
    )
    result = ExternalCLIClient(
        command=command,
        cwd=str(tmp_path),
        prompt="hello",
        stdout_max_bytes=8,
        timeout=5,
    ).run()
    assert result.status == "output_truncated"
    assert result.summary is None


def test_stderr_is_isolated_and_bounded_from_result(tmp_path):
    command = _fake_cli(
        tmp_path,
        """cat >/dev/null
printf 'diagnostic-secret\\n' >&2
printf '%s\\n' '{\"type\":\"result\",\"subtype\":\"success\",\"result\":\"clean\"}'
""",
    )
    result = ExternalCLIClient(
        command=command,
        cwd=str(tmp_path),
        prompt="hello",
        stderr_max_bytes=4,
        timeout=5,
    ).run()
    assert result.status == "completed"
    assert result.summary == "clean"
    assert result.error_detail is None


def test_cancel_event_returns_promptly_and_reaps_child_group(tmp_path):
    pid_file = tmp_path / "child.pid"
    command = _fake_cli(
        tmp_path,
        f"""echo $$ > {pid_file}
sleep 30
""",
    )
    cancel = threading.Event()
    result_holder = []
    worker = threading.Thread(
        target=lambda: result_holder.append(
            ExternalCLIClient(
                command=command,
                cwd=str(tmp_path),
                prompt="hello",
                cancel_event=cancel,
                timeout=10,
            ).run()
        )
    )
    started = time.monotonic()
    worker.start()
    for _ in range(20):
        if pid_file.exists():
            break
        time.sleep(0.01)
    assert pid_file.exists()
    cancel.set()
    worker.join(2)
    result = result_holder[0]
    assert result.status == "cancelled"
    assert time.monotonic() - started < 2.5
    pid = int(pid_file.read_text())
    for _ in range(20):
        try:
            os.kill(pid, 0)
        except ProcessLookupError:
            break
        time.sleep(0.05)
    else:
        pytest.fail(f"fake CLI process {pid} survived cancellation")


def test_concurrency_runner_rejects_excess_work_and_releases_slot():
    entered = threading.Event()
    release = threading.Event()

    class BlockingClient:
        def run(self):
            entered.set()
            release.wait(2)
            return CLIResult(status="completed", summary="done")

    runner = ConcurrentExternalCLIRunner(max_concurrent=1)
    first_result = []
    thread = threading.Thread(
        target=lambda: first_result.append(runner.run_bounded(BlockingClient()))
    )
    thread.start()
    assert entered.wait(1)
    with pytest.raises(ConcurrencyLimitError):
        runner.run_bounded(BlockingClient())
    release.set()
    thread.join(2)
    assert first_result[0].summary == "done"
    assert runner.active == 0
    assert runner.run_bounded(BlockingClient()).status == "completed"


def test_external_cli_transport_has_no_anthropic_sdk_import_or_call_path():
    source = open(
        os.path.join(os.path.dirname(__file__), "..", "agent", "external_cli_client.py"),
        encoding="utf-8",
    ).read()
    tree = ast.parse(source)
    imported = []
    called_names = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            imported.extend(alias.name for alias in node.names)
        elif isinstance(node, ast.ImportFrom) and node.module:
            imported.append(node.module)
        elif isinstance(node, ast.Call):
            if isinstance(node.func, ast.Name):
                called_names.append(node.func.id)
            elif isinstance(node.func, ast.Attribute) and isinstance(node.func.value, ast.Name):
                called_names.append(f"{node.func.value.id}.{node.func.attr}")
    assert not any(name == "anthropic" or name.startswith("anthropic.") for name in imported)
    assert not any(name.startswith("anthropic.") for name in called_names)
