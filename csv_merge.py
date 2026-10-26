#!/usr/bin/env python3
"""Merge multiple CSV files that share the same header into one CSV.

Zero dependencies: Python standard library only. Handles UTF-8 and UTF-8-with-BOM.

Examples
--------
    # Merge every CSV in ./data into merged.csv
    python csv_merge.py "data/*.csv"

    # Custom output name
    python csv_merge.py "reports/*.csv" -o all_reports.csv
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
    ap.add_argument("pattern", help="Glob pattern, e.g. 'data/*.csv'")
    ap.add_argument("-o", "--output", default="merged.csv", help="Output file")
    args = ap.parse_args()

    files = sorted(glob.glob(args.pattern))
    if not files:
        print(f"No files matched: {args.pattern}")
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
