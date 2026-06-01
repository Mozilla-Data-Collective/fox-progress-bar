import pytest
from fox_progress_bar.progress import ProgressBar


def test_update_and_finish_no_total_zero_does_not_crash(capsys):
    pb = ProgressBar(total_size=0)
    pb.update(10)
    pb.finish()
    out, _ = capsys.readouterr()
    assert "🦊" in out


def test_finish_with_total_writes_100_percent(capsys):
    total = 100
    pb = ProgressBar(total_size=total, bar_length=10)
    pb.update(total)
    pb.finish()
    out, _ = capsys.readouterr()
    assert "100.0%" in out
    assert "🦊" in out


@pytest.mark.parametrize("seconds,expected", [
    (0, "00:00"),
    (59, "00:59"),
    (60, "01:00"),
    (3599, "59:59"),
    (3600, "01:00:00"),
    (3661, "01:01:01"),
    (86399, "23:59:59"),
    (86400, "01:00:00:00"),
    (90061, "01:01:01:01"),
])
def test_format_time(seconds, expected):
    assert ProgressBar._format_time(seconds) == expected


def test_format_time_negative():
    assert ProgressBar._format_time(-1) == "--:--"