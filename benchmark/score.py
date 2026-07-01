"""Diagnostic scoring helpers (non-authoritative).

The authoritative signal is the pairwise judge (judge.py). This lexical overlap between a
plan and the revealed trajectory is only a cheap sanity check / telemetry — it is NOT used
to rank agents, because exact-token match is the wrong target (proposal §5a).
"""

from __future__ import annotations

import re

_TOK = re.compile(r"[a-z0-9]+")


def _tokens(text: str) -> set:
    return set(_TOK.findall((text or "").lower()))


def trajectory_overlap(plan, revealed) -> float:
    """Jaccard overlap of plan tokens vs. revealed-commit-subject tokens. Diagnostic only."""
    plan_toks = set()
    for item in plan or []:
        if isinstance(item, dict):
            plan_toks |= _tokens(item.get("title", "")) | _tokens(item.get("theme", ""))
        else:
            plan_toks |= _tokens(str(item))
    real_toks = set()
    for r in revealed or []:
        real_toks |= _tokens(r.get("subject", ""))
    if not plan_toks or not real_toks:
        return 0.0
    return round(len(plan_toks & real_toks) / len(plan_toks | real_toks), 3)
