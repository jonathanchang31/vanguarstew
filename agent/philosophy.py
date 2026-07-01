"""Step 1: infer the repository's "maintainer philosophy" BEFORE deciding anything.

This is the grounding step. It is not scored directly (there is no labeled "correct
philosophy") — it exists because a plan consistent with the repo's inferred direction
is the leading indicator of getting the trajectory right downstream.
"""

from __future__ import annotations

import json

SYSTEM = (
    "You are an expert analyst of open-source project maintenance. Given a snapshot of a "
    "repository's state and recent history, infer the maintainers' implicit philosophy: "
    "their values, risk tolerance, and where the project is heading. Be specific and "
    "evidence-based. Respond ONLY with JSON."
)


def infer_philosophy(context: dict, llm) -> dict:
    user = (
        "Infer the maintainer philosophy from this repository state.\n\n"
        f"{_render(context)}\n\n"
        "Return JSON with keys:\n"
        '  "summary": one-sentence characterization,\n'
        '  "values": list of guiding values (e.g. "conservative", "refactor-first", '
        '"feature-first", "perf-first", "docs-first", "stability-over-features"),\n'
        '  "merge_bar": what tends to get merged vs rejected,\n'
        '  "direction": where the codebase appears to be heading (the "idea trajectory"),\n'
        '  "evidence": list of concrete signals you used.'
    )
    stub = {
        "summary": "offline stub philosophy",
        "values": [],
        "merge_bar": "unknown (offline)",
        "direction": "unknown (offline)",
        "evidence": [],
    }
    return llm.chat_json(SYSTEM, user, stub=stub)


def _render(context: dict) -> str:
    keep = {k: context.get(k) for k in (
        "frozen_at", "recent_commits", "open_issues", "open_prs",
        "labels", "milestones", "releases", "readme_excerpt",
    )}
    return json.dumps(keep, indent=1)[:12000]
