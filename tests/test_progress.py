from fox_progress_bar.progress import ProgressBar


def test_update_and_finish_no_total_zero_does_not_crash(capsys):
    pb = ProgressBar(total_size=0)
    pb.update(10)
    pb.finish()
    out, _ = capsys.readouterr()
    assert "🦊" in out
