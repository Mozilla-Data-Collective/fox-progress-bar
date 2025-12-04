# 🦊-progress-bar

A tiny terminal progress bar with a 🦊

![demo.gif](demo.gif)

## Installation

```bash
pip install fox-progress-bar
```

## Demo

Run a demo with:
```bash
fox-progress-demo
```

## Usage

```python
from fox_progress_bar import ProgressBar
import time

total = 5_000_000
chunk_size = total // 100
pb = ProgressBar(total_size=total)
for _ in range(100):
    pb.update(chunk_size)
    time.sleep(0.03)
pb.finish()
```

> [!TIP]
> You can define your own unit of measurement to display through the `unit` parameter of `ProgressBar`. E.g.
> ```python
> pb = ProgressBar(total_size=total, unit="foxes")
> ```


## Releasing (GitHub + PyPI)

Everytime you create a GitHub Release (use a tag like v0.1.0), GitHub Actions will automatically build and publish the package to PyPI. Make sure to bump `version` in `pyproject.toml` accordingly for each release. If needed, you can also trigger a release manually from the "Actions" tab in GitHub to bypass the version check (not recommended).


## Tests

1. Ensure venv is active and install test dependencies:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e .
pip install pytest
```
2. Run tests with pytest:

```bash
pytest -q
```