# Hermes task-shape routing

`agent/routing.py` is the pure routing seam for choosing between the Hermes
coordination lane and the Codex-native lane. It intentionally produces a
privacy-safe `RoutingDecision`; callers do not need to persist the request
text.

## Signals

The classifier recognizes six stable signal names:

- `decomposition`: split, decompose, subtasks, or step-by-step work.
- `bounded_scope`: bounded/time-boxed/focused work, explicit scope or
  acceptance criteria, or a one-file/module limit.
- `dependency_coordination`: dependencies, ordering after completion,
  coordination, blocked-by relationships, or fan-in.
- `explicit_orchestration`: orchestration, workflow, parent-child, Kanban, or
  supervision language.
- `needs_parallel_children`: parallel/concurrent work, child workers, multiple
  agents, or fan-out.
- `coding_task`: implementation, fixes, refactors, patches, edits, tests, and
  repository/source/function references.

A Hermes route requires at least two independent coordination/task-shape
dimensions. Bounded scope counts as one dimension when paired with another
coordination signal; it does not route a request to Hermes by itself. A
focused coding shape routes to Codex-native. Requests that contain only weak
intent words are marked `ambiguous`; requests with no recognized evidence are
marked `fallback`. Both use the configured safe default (Codex-native by
default).

## Choosing a lane

Use the Hermes lane when the work is coordination-shaped, not merely difficult:

- Choose Hermes for a bounded workflow that must be decomposed, coordinated,
  ordered, or fanned out to child agents. For example: “Decompose this
  acceptance-tested migration into two independent checks, run them in
  parallel, then fan in the results.” This matches `decomposition`,
  `bounded_scope`, `needs_parallel_children`, and `dependency_coordination`.
- Choose Codex-native for one focused coding task, such as “Fix the parser
  regression in `agent/routing.py` and add a test.” A coding signal alone does
  not justify coordination.
- Add an explicit directive when policy matters: “Use the Hermes lane” or
  “Use the Codex-native lane.” An explicit directive wins over inferred shape;
  when both directives occur, Codex-native is the narrower safe choice.

Bounded coordination means both (a) a stated limit—time box, one file/module,
acceptance criteria, or an explicitly limited scope—and (b) at least one other
coordination dimension such as decomposition, dependencies, orchestration, or
parallel children. “Coordinate this” alone and “keep it bounded” alone are not
enough. This conservative threshold avoids paying coordination overhead for a
single-agent task.

## Safe defaults and provider fallback

The router is observational at the conversation boundary: the already
configured runtime remains the safe default, while the decision records what
the task shape recommends. `ambiguous` means weak intent was present but not
enough evidence for a lane; `fallback` means no recognized routing evidence was
present. Neither classification is, by itself, a provider failure. A provider
fallback is recorded only when the observed source differs from the intended
source or the source is `default_fallback`. OpenAI Codex Responses/fallback
targets are labelled `codex_native`; other unavailable targets use
`default_fallback`.

## Precedence

1. Explicit Hermes or Codex-native directive. If both are present, choose
   Codex-native as the narrower safe lane.
2. Multiple coordination dimensions (`hermes_task_shape`).
3. Focused coding/repository shape (`codex_native_task_shape`).
4. Safe default (`safe_default`).

## Runtime integration

Call `route_task(prompt)` before dispatch. Include
`decision.telemetry_context()` in the selection event. At completion, pass
`actual_agent_source`, `completion_status`, `outcome_quality`, and, when
needed, `fallback_reason` to the same method. The resulting fields are stable
and JSON-safe:

- `intended_route` / `route`
- `actual_agent_source` (when observed)
- `classification`, `precedence`, `reason`
- `matched_signals`, `signal_scores`, and `task_shape`
- `completion_status`, `outcome_quality`, `fallback_reason` (when observed)

Only canonical signal labels and counts are emitted; prompt text is not.

## Runtime telemetry

The `agent.routing_telemetry` module emits JSONL records to
`$HERMES_ROUTING_EVENTS_PATH` (or `~/.hermes/logs/routing-events.jsonl`) and
logs the same bounded record through `hermes.routing`. A
`routing_decision` is emitted before an `AIAgent` conversation starts; its
`decisions_total` count is the denominator for both `selection_rate`
(`hermes_selections_total / decisions_total`) and `fallback_rate`
(`fallbacks_total / decisions_total`). The decision also includes the
classifier's bounded `classification`, `precedence`, `matched_signals`, and
`task_shape_details` when available. A `fallback` or `ambiguous` classifier
result means that policy used its safe default; it is not counted as a
provider fallback unless the observed source differs from the intended route
or is `default_fallback`. A `routing_outcome` is emitted when the conversation
reaches a terminal result. `outcome_quality_rate` is good outcomes divided by
outcomes labelled `good` or `poor`; unknown and interrupted outcomes are
excluded from that denominator.

Regular conversations are labelled `hermes`; the Codex Responses/native
runtime is labelled `codex_native`. Provider failover emits a second decision
with `fallback: true`, using `codex_native` when the target is an OpenAI Codex
runtime and `default_fallback` for other fallback targets. Request and session
identifiers are one-way hashes, and telemetry errors are swallowed so an
unavailable log path cannot change routing or fail a request.

## Reading runtime and memory evidence

For one request, expect a `routing_decision` JSONL record before execution and
one `routing_outcome` record at the terminal result. Join them using their
hashed `request_id` (not the prompt). The minimum evidence for a successful
bounded-coordination turn is:

1. decision: `route_intent: "hermes"`, `selected_agent_source: "hermes"`,
   `task_shape: "bounded_coordination"`, `fallback: false`, and the expected
   canonical signals;
2. outcome: the same selected source, `outcome: "completed"`, and
   `outcome_quality: "good"`;
3. metrics: `decisions_total` and `outcomes_total` increased, with
   `fallback_rate: 0.0` for a no-fallback run.

`selection_rate` is Hermes selections divided by all routing decisions,
`fallback_rate` is provider fallbacks divided by all routing decisions, and
`outcome_quality_rate` is good outcomes divided by outcomes explicitly labelled
`good` or `poor`. Unknown and interrupted quality values are excluded rather
than treated as successes. The in-process aggregate can be inspected with
`agent.routing_telemetry.get_routing_metrics(path)`; the persisted source is
the JSONL file described above. Logging emits the same bounded JSON under
`hermes.routing`.

When agent-source outcome memory is enabled, its record should corroborate the
telemetry outcome with `intended_route`, `actual_agent_source`,
`completion_status`, and `outcome_quality`. It must not contain prompt text:
identifiers are hashed and routing fields are categorical. Memory persistence
is fail-open, so missing or broken memory must not turn a successful request
into a routing failure; treat telemetry plus the terminal result as the primary
runtime evidence.

### Reproducible smoke evidence

Run the production-boundary smoke test (it uses pytest's isolated `tmp_path`
for the event file):

```bash
PYTHONPATH=. pytest -o addopts='' \
  tests/test_routing_telemetry.py \
  -k production_conversation_entrypoint_smoke -q
```

The test drives a realistic bounded-coordination request through
`conversation_loop.run_conversation`, then asserts the decision, outcome,
metrics, and agent-source memory evidence. For an event file captured from a
live turn, set `HERMES_ROUTING_EVENTS_PATH` before starting Hermes. Inspect it
without exposing prompt content:

```bash
python -c 'import json; [print(json.dumps(json.loads(line), sort_keys=True)) for line in open("/tmp/hermes-routing-events.jsonl") if line.strip()]'
```
