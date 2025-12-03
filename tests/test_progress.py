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