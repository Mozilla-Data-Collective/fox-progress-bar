# A simple demo CLI to showcase the ProgressBar

import time
from .progress import ProgressBar


def main() -> None:
    total = 10_000_000
    pb = ProgressBar(total_size=total)
    chunks = 200
    per_chunk = total // chunks
    for _ in range(chunks):
        pb.update(per_chunk)
        time.sleep(0.02)
    pb.finish()
