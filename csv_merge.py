#!/usr/bin/env python3
"""Merge multiple CSV files that share the same header into one CSV.

Zero dependencies: Python standard library only. Handles UTF-8 and UTF-8-with-BOM.

Accepts one or more arguments; each may be a glob pattern or a literal path.
Quote your globs in bash so the shell does not expand them first.

Examples
--------
    # Merge every CSV in ./data into merged.csv (pattern handled by the script)
    python csv_merge.py "data/*.csv"

    # Custom output name
    python csv_merge.py "reports/*.csv" -o all_reports.csv

    # Several explicit files or patterns (also fine if your shell already expanded them)
    python csv_merge.py a.csv b.csv -o merged.csv
"""
import argparse
import csv
import glob
import os
import sys


def main() -> int:
    ap = argparse.ArgumentParser(
        description="Merge CSV files with the same header into one."
    )
    ap.add_argument(
        "patterns",
        nargs="+",
        help="One or more glob patterns or file paths, e.g. 'data/*.csv'",
    )
    ap.add_argument("-o", "--output", default="merged.csv", help="Output file")
    args = ap.parse_args()

    files = []
    for pat in args.patterns:
        matched = sorted(glob.glob(pat))
        if not matched and os.path.exists(pat):
            matched = [pat]
        if not matched:
            print(f"No files matched: {pat}", file=sys.stderr)
        files.extend(matched)
    files = sorted(set(files))
    if not files:
        print("No files matched any pattern.")
        return 1

    header = None
    count = 0
    with open(args.output, "w", newline="", encoding="utf-8") as out:
        w = csv.writer(out)
        for fp in files:
            try:
                with open(fp, "r", newline="", encoding="utf-8-sig") as f:
                    rows = list(csv.reader(f))
            except OSError as e:
                print(f"skip {fp}: {e}", file=sys.stderr)
                continue
            if not rows:
                continue
            if header is None:
                header = rows[0]
                w.writerow(header)
            elif rows[0] != header:
                print(f"WARN: header mismatch in {fp}; skipping its header row",
                      file=sys.stderr)
            for row in rows[1:]:
                w.writerow(row)
                count += 1

    print(f"Merged {len(files)} file(s) -> {args.output} ({count} data rows).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
