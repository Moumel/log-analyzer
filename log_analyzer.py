
import argparse
import json
import logging
import sys
from collections import Counter
from pathlib import Path


logger = logging.getLogger(__name__)

VALID_LEVELS = ("INFO", "WARNING", "ERROR")

LEVEL_PRIORITY = {
    "INFO": 1,
    "WARNING": 2,
    "ERROR": 3,
}


def parse_log_line(line):
    """Parse one log line.

    Expected format:
    YYYY-MM-DD HH:MM:SS LEVEL message
    """
    parts = line.strip().split(maxsplit=3)

    if len(parts) != 4:
        return None

    date, time, level, message = parts

    if level not in VALID_LEVELS:
        return None

    return level, message


def analyze_logs(file_paths, level=None):
    """Analyze one or more log files and return a report."""

    if level is not None:
        level = level.upper()

        if level not in VALID_LEVELS:
            raise ValueError(
                f"Invalid level: {level}. "
                f"Choose from: {', '.join(VALID_LEVELS)}"
            )

    counts = Counter()
    errors = []
    warnings = []
    broken_lines = []

    total_lines = 0
    files_analyzed = 0

    for file_path in file_paths:
        path = Path(file_path)

        if not path.exists():
            logger.error("File not found: %s", path)
            raise FileNotFoundError(f"File not found: {path}")

        if not path.is_file():
            logger.error("Not a file: %s", path)
            raise IsADirectoryError(f"Not a file: {path}")

        logger.debug("Analyzing file: %s", path)
        files_analyzed += 1

        with path.open("r", encoding="utf-8") as file:
            for line_number, line in enumerate(file, start=1):

                if not line.strip():
                    continue

                total_lines += 1
                parsed = parse_log_line(line)

                if parsed is None:
                    logger.warning(
                        "Malformed line in %s at line %s",
                        path,
                        line_number,
                    )

                    broken_lines.append({
                        "file": str(path),
                        "line": line_number,
                        "content": line.strip(),
                    })
                    continue

                log_level, message = parsed

                # Apply minimum severity filtering.
                if level and LEVEL_PRIORITY[log_level] < LEVEL_PRIORITY[level]:
                    continue

                counts[log_level] += 1

                entry = {
                    "file": str(path),
                    "line": line_number,
                    "message": message,
                }

                if log_level == "ERROR":
                    errors.append(entry)

                elif log_level == "WARNING":
                    warnings.append(entry)

    logger.info(
        "Analysis completed. Processed %s file(s).",
        files_analyzed,
    )

    return {
        "files_analyzed": files_analyzed,
        "total_lines": total_lines,
        "counts": {
            "INFO": counts["INFO"],
            "WARNING": counts["WARNING"],
            "ERROR": counts["ERROR"],
        },
        "errors": errors,
        "warnings": warnings,
        "broken_lines": broken_lines,
    }


def print_report(report):
    """Print the analysis report."""

    print("\nLog Analysis Report")
    print("-------------------")

    print(f"Files analyzed: {report['files_analyzed']}")
    print(f"Total lines: {report['total_lines']}")

    for level in VALID_LEVELS:
        print(f"{level}: {report['counts'][level]}")

    print(f"Broken lines: {len(report['broken_lines'])}")

    print("\nErrors:")

    if report["errors"]:
        for entry in report["errors"]:
            print(
                f"- {entry['file']}:{entry['line']}: "
                f"{entry['message']}"
            )
    else:
        print("No errors found.")

    print("\nWarnings:")

    if report["warnings"]:
        for entry in report["warnings"]:
            print(
                f"- {entry['file']}:{entry['line']}: "
                f"{entry['message']}"
            )
    else:
        print("No warnings found.")

    print("\nBroken lines:")

    if report["broken_lines"]:
        for entry in report["broken_lines"]:
            print(
                f"- {entry['file']}:{entry['line']}: "
                f"{entry['content']}"
            )
    else:
        print("No broken lines found.")


def write_json_report(report, output_path):
    """Save the report as a JSON file."""

    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)

    with path.open("w", encoding="utf-8") as file:
        json.dump(report, file, indent=4, ensure_ascii=False)

    logger.info("JSON report saved to %s", path)


def build_parser():
    parser = argparse.ArgumentParser(
        description="Analyze one or more log files."
    )

    parser.add_argument(
        "files",
        nargs="+",
        help="One or more log files to analyze.",
    )

    parser.add_argument(
        "--level",
        choices=VALID_LEVELS,
        help="Show logs at this severity level or higher.",
    )

    parser.add_argument(
        "--output",
        help="Save the report as a JSON file.",
    )

    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Show detailed diagnostic logging.",
    )

    return parser


def main():
    parser = build_parser()
    args = parser.parse_args()

    logging.basicConfig(
        level=logging.DEBUG if args.verbose else logging.WARNING,
        format="%(levelname)s: %(message)s",
    )

    try:
        report = analyze_logs(args.files, level=args.level)

        print_report(report)

        if args.output:
            write_json_report(report, args.output)
            print(f"\nJSON report saved to: {args.output}")

        return 0

    except (FileNotFoundError, IsADirectoryError, ValueError, OSError) as error:
        logger.error("%s", error)
        print(f"Error: {error}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
