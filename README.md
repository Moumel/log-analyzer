# Python Log Analyzer

![Tests](https://github.com/Moumel/log-analyzer/actions/workflows/tests.yml/badge.svg)

A command-line tool for analyzing application and server log files.

It counts log levels, detects malformed entries, filters messages by severity, and exports analysis reports as JSON.

## Features

- Analyze one or multiple log files in a single run.
- Count INFO, WARNING, and ERROR messages.
- Filter messages by minimum severity level.
- Detect malformed log entries.
- Export reports to JSON.
- Diagnostic logging with Python's `logging` module.
- Automated tests with pytest. Test coverage: **XX%** (update this number).
- Continuous Integration with GitHub Actions.

## Requirements

- Python 3.10 or newer
- pip

## Installation

Clone the repository:

```bash
git clone https://github.com/Moumel/log-analyzer.git
cd log-analyzer
```

Create and activate a virtual environment.

Windows (PowerShell):

```powershell
py -m venv .venv
.venv\Scripts\Activate.ps1
```

Linux / macOS:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Install dependencies:

```bash
python -m pip install -r requirements.txt
```

## Log Format

The analyzer expects one entry per line:

```text
2026-11-07 12:00:01 ERROR Database connection failed
```

Format: `YYYY-MM-DD HH:MM:SS LEVEL message`, where LEVEL is `INFO`, `WARNING`, or `ERROR`.

A line is counted as **malformed** if it has no valid timestamp or no valid level. Malformed lines are reported separately and do not stop the analysis.

## Usage

On Windows, use `py` instead of `python`.

Analyze a single log file:

```bash
python log_analyzer.py logs/server.log
```

Analyze multiple log files:

```bash
python log_analyzer.py logs/server.log logs/application.log
```

Show only errors:

```bash
python log_analyzer.py logs/server.log --level ERROR
```

Show warnings and errors:

```bash
python log_analyzer.py logs/server.log --level WARNING
```

Export the report as JSON:

```bash
python log_analyzer.py logs/server.log --output reports/report.json
```

Enable detailed diagnostic logging:

```bash
python log_analyzer.py logs/server.log --verbose
```

## Testing

Run the automated test suite:

```bash
python -m pytest -v
```

Run tests with coverage:

```bash
python -m pytest -v --cov=log_analyzer --cov-report=term-missing
```

## Project Structure

```text
log-analyzer/
├── .github/workflows/tests.yml
├── logs/
│   ├── server.log
│   └── application.log
├── reports/
├── log_analyzer.py
├── test_log_analyzer.py
├── requirements.txt
├── README.md
└── .gitignore
```

Built with Python, argparse, logging, pathlib, pytest, pytest-cov, and GitHub Actions.
