"""Generate replay tasks from a repo's git history (our fork of ninja's `Generate`).

Ninja picks one commit and asks the agent to reproduce it. We instead pick a freeze
point T with enough history before it and at least `horizon` commits after it, and treat
those next-N commits as the **revealed maintainer actions** — the reference trajectory.
"""

from __future__ import annotations

from benchmark.freeze import _git


def linear_history(repo: str) -> list:
    """First-parent commit shas, oldest -> newest."""
    out = _git(repo, "rev-list", "--first-parent", "--reverse", "HEAD")
    return [line for line in out.splitlines() if line]


def revealed_window(repo: str, commits: list, idx: int, n: int) -> list:
    """The next `n` maintainer actions after the freeze commit (the reference)."""
    window = []
    for sha in commits[idx + 1: idx + 1 + n]:
        subject = _git(repo, "log", "-1", "--pretty=format:%s", sha).strip()
        files = _git(repo, "show", "--name-only", "--pretty=format:", sha, check=False).split()
        window.append({"sha": sha[:10], "subject": subject, "files": files[:20]})
    return window


def generate_tasks(repo: str, num_tasks: int = 3, horizon: int = 5, min_history: int = 10) -> list:
    commits = linear_history(repo)
    usable = [i for i in range(len(commits)) if i >= min_history and i + horizon < len(commits)]
    if not usable:
        return []
    step = max(1, len(usable) // max(1, num_tasks))
    picks = usable[::step][:num_tasks]
    tasks = []
    for i in picks:
        tasks.append({
            "freeze_commit": commits[i],
            "freeze_index": i,
            "revealed": revealed_window(repo, commits, i, horizon),
        })
    return tasks
