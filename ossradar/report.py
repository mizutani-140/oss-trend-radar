"""Render trend reports as Markdown."""

from __future__ import annotations

import datetime
from collections.abc import Sequence

from .models import Repo


def _format_delta(delta: int | None) -> str:
    """Render a star delta for the report: ▲/▼/±0, or 'new' when no prior data."""
    if delta is None:
        return "new"
    if delta > 0:
        return f"▲ +{delta:,}"
    if delta < 0:
        return f"▼ {delta:,}"
    return "±0"


def format_report(
    repos: Sequence[Repo],
    generated_on: datetime.date,
    deltas: dict[str, int | None] | None = None,
) -> str:
    """Render the trending repositories as a dated Markdown report.

    When ``deltas`` is provided, a "Δ Stars" column shows each repo's star
    change versus the previous snapshot (or "new" for first-seen repos).
    """
    lines: list[str] = [
        f"# OSS Trend Radar — {generated_on.isoformat()}",
        "",
        f"Top {len(repos)} trending repositories by stars.",
        "",
    ]

    if not repos:
        lines.append("_No repositories found._")
        return "\n".join(lines) + "\n"

    if deltas is None:
        lines.append("| # | Repository | Stars | Language | Description |")
        lines.append("| - | ---------- | ----- | -------- | ----------- |")
    else:
        lines.append("| # | Repository | Stars | Δ Stars | Language | Description |")
        lines.append("| - | ---------- | ----- | ------- | -------- | ----------- |")

    for rank, repo in enumerate(repos, start=1):
        language = repo.language or "—"
        description = (repo.description or "").replace("|", "\\|").replace("\n", " ")
        if deltas is None:
            lines.append(
                f"| {rank} "
                f"| [{repo.full_name}]({repo.url}) "
                f"| {repo.stars:,} "
                f"| {language} "
                f"| {description} |"
            )
        else:
            lines.append(
                f"| {rank} "
                f"| [{repo.full_name}]({repo.url}) "
                f"| {repo.stars:,} "
                f"| {_format_delta(deltas.get(repo.full_name))} "
                f"| {language} "
                f"| {description} |"
            )

    return "\n".join(lines) + "\n"
