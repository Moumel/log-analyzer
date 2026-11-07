
import json

import pytest

from log_analyzer import (
    analyze_logs,
    parse_log_line,
    write_json_report,
)


@pytest.fixture
def sample_log(tmp_path):
    log_file = tmp_path / "test.log"

    log_file.write_text(
        "2026-01-01 10:00:00 INFO Application started\n"
        "2026-01-01 10:01:00 WARNING Disk space low\n"
        "2026-01-01 10:02:00 ERROR Connection failed\n"
        "This is a broken line\n"
        "2026-01-01 10:03:00 ERROR Database unavailable\n",
        encoding="utf-8",
    )

    return log_file


def test_parse_valid_log_line():
    result = parse_log_line(
        "2026-01-01 10:00:00 INFO Application started"
    )

    assert result == ("INFO", "Application started")


def test_parse_warning_log_line():
    result = parse_log_line(
        "2026-01-01 10:00:00 WARNING Disk space low"
    )

    assert result == ("WARNING", "Disk space low")


def test_parse_invalid_log_line():
    assert parse_log_line("This is a broken line") is None


def test_analyze_counts(sample_log):
    report = analyze_logs([sample_log])

    assert report["counts"]["INFO"] == 1
    assert report["counts"]["WARNING"] == 1
    assert report["counts"]["ERROR"] == 2


def test_analyze_total_lines(sample_log):
    report = analyze_logs([sample_log])

    assert report["total_lines"] == 5


def test_analyze_broken_lines(sample_log):
    report = analyze_logs([sample_log])

    assert len(report["broken_lines"]) == 1


def test_analyze_errors(sample_log):
    report = analyze_logs([sample_log])

    assert len(report["errors"]) == 2


def test_analyze_warnings(sample_log):
    report = analyze_logs([sample_log])

    assert len(report["warnings"]) == 1


def test_error_level_filter(sample_log):
    report = analyze_logs([sample_log], level="ERROR")

    assert report["counts"]["INFO"] == 0
    assert report["counts"]["WARNING"] == 0
    assert report["counts"]["ERROR"] == 2


def test_warning_level_filter(sample_log):
    report = analyze_logs([sample_log], level="WARNING")

    assert report["counts"]["INFO"] == 0
    assert report["counts"]["WARNING"] == 1
    assert report["counts"]["ERROR"] == 2


def test_info_level_filter(sample_log):
    report = analyze_logs([sample_log], level="INFO")

    assert report["counts"]["INFO"] == 1
    assert report["counts"]["WARNING"] == 1
    assert report["counts"]["ERROR"] == 2


def test_invalid_level(sample_log):
    with pytest.raises(ValueError):
        analyze_logs([sample_log], level="DEBUG")


def test_missing_file():
    with pytest.raises(FileNotFoundError):
        analyze_logs(["missing.log"])


def test_multiple_files(tmp_path):
    file_one = tmp_path / "one.log"
    file_two = tmp_path / "two.log"

    file_one.write_text(
        "2026-01-01 10:00:00 INFO First file\n",
        encoding="utf-8",
    )

    file_two.write_text(
        "2026-01-01 10:01:00 ERROR Second file\n",
        encoding="utf-8",
    )

    report = analyze_logs([file_one, file_two])

    assert report["files_analyzed"] == 2
    assert report["counts"]["INFO"] == 1
    assert report["counts"]["ERROR"] == 1


def test_json_report_export(sample_log, tmp_path):
    report = analyze_logs([sample_log])

    output_file = tmp_path / "reports" / "report.json"

    write_json_report(report, output_file)

    assert output_file.exists()

    saved_report = json.loads(
        output_file.read_text(encoding="utf-8")
    )

    assert saved_report["counts"]["ERROR"] == 2


def test_empty_file(tmp_path):
    empty_file = tmp_path / "empty.log"
    empty_file.write_text("", encoding="utf-8")

    report = analyze_logs([empty_file])

    assert report["total_lines"] == 0
    assert report["counts"]["INFO"] == 0
    assert report["counts"]["ERROR"] == 0


def test_blank_lines_are_ignored(tmp_path):
    log_file = tmp_path / "blank.log"

    log_file.write_text(
        "\n"
        "2026-01-01 10:00:00 INFO Started\n"
        "\n",
        encoding="utf-8",
    )

    report = analyze_logs([log_file])

    assert report["total_lines"] == 1
    assert report["counts"]["INFO"] == 1
