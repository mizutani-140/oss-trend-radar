"""CLI orchestration: fetch trending repos and write a Markdown report."""

from __future__ import annotations

import argparse
import datetime
import os
from pathlib import Path

from .github import DEFAULT_QUERY, fetch_trending
from .report import format_report


def run_report(
    *,
    query: str = DEFAULT_QUERY,
    top: int = 10,
    out_dir: str | Path = "reports",
    today: datetime.date | None = None,
) -> Path:
    """Fetch trending repos and write reports/<date>.md. Returns the file path."""
    today = today or datetime.date.today()
    token = os.environ.get("GITHUB_TOKEN")

    repos = fetch_trending(query, top=top, token=token)
    markdown = format_report(repos, generated_on=today)

    out_path = Path(out_dir)
    out_path.mkdir(parents=True, exist_ok=True)
    report_file = out_path / f"{today.isoformat()}.md"
    report_file.write_text(markdown, encoding="utf-8")
    return report_file


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="ossradar", description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)

    report = sub.add_parser("report", help="Generate a Markdown trend report")
    report.add_argument("--query", default=DEFAULT_QUERY, help="GitHub search query")
    report.add_argument("--top", type=int, default=10, help="Number of repos")
    report.add_argument("--out-dir", default="reports", help="Output directory")
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    if args.command == "report":
        path = run_report(query=args.query, top=args.top, out_dir=args.out_dir)
        print(f"Wrote {path}")
        return 0

    parser.error(f"unknown command: {args.command}")
    return 2
