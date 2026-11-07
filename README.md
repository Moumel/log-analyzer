# Log Analyzer with Tests and CI

A Python command-line tool that analyzes log files, counts INFO/WARNING/ERROR entries, identifies malformed lines, and prints a summary report.

## Requirements

- Python 3.10+
- pip

## Open in Visual Studio Code

1. Extract or clone this repository.
2. Open the `log-analyzer` folder in Visual Studio Code.
3. Open the integrated terminal (**Terminal → New Terminal**).
4. Create and activate a virtual environment (optional but recommended):

   **Windows PowerShell**
   ```powershell
   python -m venv .venv
   .\.venv\Scripts\Activate.ps1
   ```

   **Windows Command Prompt**
   ```bat
   python -m venv .venv
   .venv\Scripts\activate.bat
   ```

   **macOS/Linux**
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```

5. Install dependencies:
   ```bash
   python -m pip install -r requirements.txt
   ```

## Run the analyzer

```bash
python log_analyzer.py server.log
```

## Example output

```text
Log Analysis Report
------------------
Total lines: 5
INFO: 2
WARNING: 1
ERROR: 2
Broken lines: 0

Errors:
- Line 3: Connection failed
- Line 5: Database unavailable

Warnings:
- Line 2: Disk space low
```

## Run tests

```bash
pytest -v
```

## GitHub Actions

The workflow in `.github/workflows/tests.yml` runs pytest on every push and pull request.

## Log format

Each non-empty line should follow this format:

```text
YYYY-MM-DD HH:MM:SS LEVEL message
```

Supported levels: `INFO`, `WARNING`, `ERROR`.

Malformed lines and unsupported levels are listed as broken lines. Blank lines are ignored.

## Technologies

Python, pytest, Git, GitHub Actions.
