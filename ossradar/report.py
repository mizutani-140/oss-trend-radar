"""Render trend reports as Markdown."""

from __future__ import annotations

import datetime
from collections.abc import Sequence

from .models import Repo


def format_report(repos: Sequence[Repo], generated_on: datetime.date) -> str:
    """Render the trending repositories as a dated Markdown report."""
    lines: list[str] = [
        f"# OSS Trend Radar — {generated_on.isoformat()}",
        "",
        f"Top {len(repos)} trending repositories by stars.",
        "",
    ]

    if not repos:
        lines.append("_No repositories found._")
        return "\n".join(lines) + "\n"

    lines.append("| # | Repository | Stars | Language | Description |")
    lines.append("| - | ---------- | ----- | -------- | ----------- |")
    for rank, repo in enumerate(repos, start=1):
        language = repo.language or "—"
        description = (repo.description or "").replace("|", "\\|").replace("\n", " ")
        lines.append(
            f"| {rank} "
            f"| [{repo.full_name}]({repo.url}) "
            f"| {repo.stars:,} "
            f"| {language} "
            f"| {description} |"
        )

    return "\n".join(lines) + "\n"
