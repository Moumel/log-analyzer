
# Python Log Analyzer

A command-line tool for analyzing application and server log files.

The tool identifies log levels, detects malformed entries, filters
messages by severity, and exports analysis reports as JSON.

## Features

- Analyze one or multiple log files.
- Count INFO, WARNING, and ERROR messages.
- Filter messages by minimum severity level.
- Detect malformed log entries.
- Export reports to JSON.
- Diagnostic logging with Python's logging module.
- Automated tests using pytest.
- Test coverage using pytest-cov.
- Continuous Integration using GitHub Actions.

## Project Structure

```text
log-analyzer/
│
├── .github/
│   └── workflows/
│       └── tests.yml
│
├── logs/
│   ├── server.log
│   └── application.log
│
├── reports/
│
├── log_analyzer.py
├── test_log_analyzer.py
├── requirements.txt
├── README.md
└── .gitignore
```

## Requirements

- Python 3.10 or newer
- pip

## Installation

Clone the repository:

```bash
git clone <https://github.com/Moumel/log-analyzer>
cd log-analyzer
```

Create a virtual environment:

```bash
py -m venv .venv
```

Activate it on Windows PowerShell:

```powershell
.venv\Scripts\Activate.ps1
```

Install dependencies:

```bash
py -m pip install -r requirements.txt
```

## Usage

Analyze a single log file:

```bash
py log_analyzer.py server.log
```

Analyze multiple log files:

```bash
py log_analyzer.py server.log application.log
```

Show only errors:

```bash
py log_analyzer.py server.log --level ERROR
```

Show warnings and errors:

```bash
py log_analyzer.py server.log --level WARNING
```

Export the report as JSON:

```bash
py log_analyzer.py server.log --output reports/report.json
```

Enable detailed diagnostic logging:

```bash
py log_analyzer.py server.log --verbose
```

## Testing

Run the automated test suite:

```bash
py -m pytest -v
```

Run tests with coverage:

```bash
py -m pytest -v --cov=log_analyzer --cov-report=term-missing
```

## Technologies

- Python
- argparse
- logging
- JSON
- pathlib
- pytest
- pytest-cov
- GitHub Actions
- Git

## Learning Objectives

This project demonstrates practical experience with:

- Python scripting and automation.
- Command-line application development.
- Log analysis and troubleshooting.
- File handling and JSON reporting.
- Exception handling.
- Unit testing.
- Test coverage.
- Continuous Integration.
