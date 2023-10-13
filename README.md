# timing-utils

Small timing helpers (decorator + context manager).

## Install

Install from source:

```bash
git clone <repo-url>
cd <repo-name>
python -m venv .venv
. .venv/bin/activate
python -m pip install -U pip
python -m pip install .
```

## Usage

```python
from timing_utils import time_call, timed, timed_context

@timed
def work():
    return 42

with timed_context("load-data"):
    work()

result, elapsed = time_call(work)
```

## Development

```bash
python -m venv .venv
. .venv/bin/activate
python -m pip install -U pip
python -m pip install -e ".[dev]"
pytest
```
