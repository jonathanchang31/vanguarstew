## Issue #97

`Split unrelated planner and scoring changes into focused PRs`

This repository state already satisfies the acceptance criteria from
`gittensor-vanguard/vanguarstew#97`:

- `benchmark/freeze.py` keeps the frozen-release fix scoped to chronological
  tag ordering for the `releases` window.
- `tests/test_freeze.py` covers chronological ordering, the ten-most-recent
  selection rule, and a non-lexicographic regression case.
- `agent/planner.py` contains the explicit-PR-number matching behavior, with
  focused coverage in `tests/test_planner.py` for explicit references, stale
  references, and fuzzy-match fallback behavior.
- `benchmark/score.py` contains the weighted-module-recall path, with focused
  coverage in `tests/test_compose.py` showing both `objective_component()`
  behavior and end-to-end composite-score impact.

Related implementation history in this fork:

- `2b93508` — frozen release ordering (`#90` scope)
- `9095888` — planner PR-number matching (`#93`)
- `d03faf9` — weighted module recall in composite scoring (`#91`)
