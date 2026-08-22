# Project Backlog Recommendations (absorbed note)

Preserved details from the former `project-backlog-recommendations` skill.

## Goal
Create durable, actionable backlog entries that preserve the source review’s intent, priority, and order while adding enough execution and closeout criteria that a future implementation agent can complete and verify the work without re-reading the whole session.

## Source capture pattern
```sh
tmux capture-pane -t <target> -p -S -50000 > /tmp/<project>_<target>.txt
```

Search captures for `recommend`, `P0`, `P1`, `P2`, `critical`, `high`, `medium`, `TODO`, and `code review`.

If the pane contains only runtime logs, inspect nearby repo review artifacts such as `docs/reports/*review*.md` or `docs/archive/*review*.md` before asking the user to repeat recommendations.

## Shared backlog CLI pattern
```sh
python3 ~/.agent-commons/backlog/backlog.py --actor hermes add \
  "Recommendation title" \
  --project <project> \
  --priority high \
  --tag code-review \
  --provenance "docs/reports/review.md:P0; tmux:0:8.0" \
  --description "Why this recommendation matters." \
  --execution "Trace the existing implementation path and identify the exact integration point." \
  --execution "Implement the change with tests covering the reviewed risk." \
  --closeout "Relevant tests or CI pass with evidence." \
  --closeout "A reviewer can inspect the resulting artifact/log/UI/API and see the intended behavior."
```

## Pitfalls
- Do not stop at a prose summary when the user asked to create backlog items.
- Do not let unrelated remembered project IDs override the user’s named project.
- Do not capture transient environment failures as backlog recommendations unless the recommendation is about hardening that failure mode.
