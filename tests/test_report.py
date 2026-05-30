import datetime

from ossradar.models import Repo
from ossradar.report import format_report


def _sample_repos():
    return [
        Repo(
            full_name="octocat/hello-world",
            stars=12345,
            language="Python",
            description="A sample trending repository",
            url="https://github.com/octocat/hello-world",
        ),
        Repo(
            full_name="acme/widgets",
            stars=987,
            language=None,
            description=None,
            url="https://github.com/acme/widgets",
        ),
    ]


def test_format_report_includes_repo_name_stars_and_url():
    report = format_report(_sample_repos(), generated_on=datetime.date(2026, 5, 29))

    # Acceptance: report contains each repo's name, star count, and URL.
    assert "octocat/hello-world" in report
    assert "12,345" in report
    assert "https://github.com/octocat/hello-world" in report
    assert "acme/widgets" in report
    assert "987" in report
    assert "https://github.com/acme/widgets" in report


def test_format_report_has_dated_header():
    report = format_report(_sample_repos(), generated_on=datetime.date(2026, 5, 29))
    first_line = report.splitlines()[0]
    assert "2026-05-29" in first_line


def test_format_report_ranks_repos_in_order():
    report = format_report(_sample_repos(), generated_on=datetime.date(2026, 5, 29))
    pos_first = report.index("octocat/hello-world")
    pos_second = report.index("acme/widgets")
    assert pos_first < pos_second


def test_format_report_handles_missing_language_and_description():
    report = format_report(_sample_repos(), generated_on=datetime.date(2026, 5, 29))
    # Should not crash and should still render the second repo.
    assert "acme/widgets" in report


def test_format_report_empty_list_still_dated():
    report = format_report([], generated_on=datetime.date(2026, 5, 29))
    assert "2026-05-29" in report


def test_format_report_with_deltas_shows_increase_and_new():
    deltas = {"octocat/hello-world": 345, "acme/widgets": None}
    report = format_report(_sample_repos(), generated_on=datetime.date(2026, 5, 29), deltas=deltas)
    assert "▲" in report
    assert "+345" in report
    assert "new" in report


def test_format_report_with_negative_and_zero_delta():
    deltas = {"octocat/hello-world": -10, "acme/widgets": 0}
    report = format_report(_sample_repos(), generated_on=datetime.date(2026, 5, 29), deltas=deltas)
    assert "▼" in report


def test_format_report_without_deltas_is_backward_compatible():
    report = format_report(_sample_repos(), generated_on=datetime.date(2026, 5, 29))
    assert "Δ" not in report
