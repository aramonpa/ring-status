# Ring Status

Automatic monitor for Nordschleife track status using computer vision and color detection.

## Features

- Fetches real-time snapshots from the Nordschleife webcam
- Analyzes traffic light colors to determine track status
- Detects track conditions:
  - 🟢 **Green** (Open)
  - 🟡 **Yellow** (Caution)
  - 🔴 **Closed** (Closed)
  - ❓ **Unknown** (Unknown status)
- Respects operating hours (weekday vs weekend)

## Project Structure

```
ring-status/
├── app/                     # Main package
│   ├── __init__.py          # Package initializer
│   ├── main.py              # CLI entry point
│   ├── app.py               # Core logic
│   └── config.py            # Configuration
├── tests/                   # Unit tests
│   ├── __init__.py
│   └── test_app.py
├── .gitignore               # Git exclusions
├── LICENSE                  # MIT License
├── pyproject.toml           # Project configuration
└── README.md                # This file
```

## Requirements

- Python >= 3.9
- Dependencies listed in `pyproject.toml`

## Installation

```bash
# Installation with base dependencies
pip install -e .

# Installation with development dependencies (tests, linting, etc.)
pip install -e ".[dev]"
```

## Usage

### Command Line

```bash
# Option 1: Using the entry script
ring-status

# Option 2: Using main.py
python -m app.main

# Option 3: Importing directly
python -c "from app import check_track; check_track()"
```

### From Python

```python
from app import check_track

check_track()
```

## Configuration

Edit `app/config.py` to customize:

- **URLs**: Panomax API and snapshot base URLs
- **Hours**: Operating hours (weekday vs weekend)
- **ROI**: Region of interest coordinates in snapshots
- **HSV Masks**: Color ranges for traffic light detection
- **Threshold**: Pixel detection threshold

## Development

### Running Tests

```bash
pytest
```

### With Coverage

```bash
pytest --cov=app
```

### Code Formatting

```bash
# Black (code formatter)
black app tests

# isort (import sorter)
isort app tests

# Linting with flake8
flake8 app tests

# Type checking with mypy
mypy app
```

## License

MIT License - See [LICENSE](LICENSE) for details.