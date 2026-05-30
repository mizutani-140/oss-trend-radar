"""Persist machine-readable star snapshots and compute star deltas."""

from __future__ import annotations

import datetime
import json
from collections.abc import Sequence
from pathlib import Path

from .models import Repo


def _data_dir(out_dir: str | Path) -> Path:
    return Path(out_dir) / "data"


def write_snapshot(repos: Sequence[Repo], *, out_dir: str | Path, on_date: datetime.date) -> Path:
    """Write a JSON snapshot of {full_name: stars} to reports/data/<date>.json."""
    data_dir = _data_dir(out_dir)
    data_dir.mkdir(parents=True, exist_ok=True)
    path = data_dir / f"{on_date.isoformat()}.json"
    payload = {repo.full_name: repo.stars for repo in repos}
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    return path


def load_latest_snapshot(out_dir: str | Path, *, before: datetime.date) -> dict[str, int] | None:
    """Return the {full_name: stars} of the most recent snapshot strictly before `before`."""
    data_dir = _data_dir(out_dir)
    if not data_dir.is_dir():
        return None

    candidates: list[tuple[datetime.date, Path]] = []
    for path in data_dir.glob("*.json"):
        try:
            day = datetime.date.fromisoformat(path.stem)
        except ValueError:
            continue
        if day < before:
            candidates.append((day, path))

    if not candidates:
        return None

    _, latest = max(candidates, key=lambda pair: pair[0])
    return json.loads(latest.read_text(encoding="utf-8"))


def compute_deltas(
    repos: Sequence[Repo], prior: dict[str, int] | None
) -> dict[str, int | None]:
    """Star delta per repo vs `prior`. None means no prior data (new entry)."""
    deltas: dict[str, int | None] = {}
    for repo in repos:
        if prior is not None and repo.full_name in prior:
            deltas[repo.full_name] = repo.stars - prior[repo.full_name]
        else:
            deltas[repo.full_name] = None
    return deltas
