import datetime
from pathlib import Path

from ossradar.models import Repo
from ossradar.snapshot import compute_deltas, load_latest_snapshot, write_snapshot


def _repos():
    return [
        Repo("a/one", 100, "Python", "d", "https://github.com/a/one"),
        Repo("b/two", 50, None, None, "https://github.com/b/two"),
    ]


def test_write_snapshot_path_and_load(tmp_path):
    path = write_snapshot(_repos(), out_dir=tmp_path, on_date=datetime.date(2026, 5, 29))
    assert path == Path(tmp_path) / "data" / "2026-05-29.json"
    assert path.exists()
    snap = load_latest_snapshot(tmp_path, before=datetime.date(2026, 5, 30))
    assert snap == {"a/one": 100, "b/two": 50}


def test_load_latest_picks_most_recent_before(tmp_path):
    write_snapshot([Repo("a/one", 100, None, None, "u")], out_dir=tmp_path, on_date=datetime.date(2026, 5, 27))
    write_snapshot([Repo("a/one", 120, None, None, "u")], out_dir=tmp_path, on_date=datetime.date(2026, 5, 28))
    snap = load_latest_snapshot(tmp_path, before=datetime.date(2026, 5, 29))
    assert snap == {"a/one": 120}


def test_load_excludes_on_or_after_before(tmp_path):
    write_snapshot([Repo("a/one", 100, None, None, "u")], out_dir=tmp_path, on_date=datetime.date(2026, 5, 29))
    assert load_latest_snapshot(tmp_path, before=datetime.date(2026, 5, 29)) is None


def test_load_none_when_no_snapshots(tmp_path):
    assert load_latest_snapshot(tmp_path, before=datetime.date(2026, 5, 29)) is None


def test_compute_deltas_existing_repos():
    deltas = compute_deltas(_repos(), {"a/one": 90, "b/two": 50})
    assert deltas == {"a/one": 10, "b/two": 0}


def test_compute_deltas_new_repo_is_none():
    deltas = compute_deltas([Repo("c/new", 5, None, None, "u")], {"a/one": 1})
    assert deltas == {"c/new": None}


def test_compute_deltas_no_prior_all_none():
    deltas = compute_deltas([Repo("a/one", 5, None, None, "u")], None)
    assert deltas == {"a/one": None}
