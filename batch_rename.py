#!/usr/bin/env python3
"""Batch rename files in a folder by a regex pattern.

Dry-run by default (safe). Add --apply to actually rename.

Zero dependencies: Python standard library only.

Examples
--------
    # Preview: turn "IMG_20240101_xxx.jpg" -> "photo_20240101_xxx.jpg"
    python batch_rename.py "C:/Photos" --pattern "IMG_(\\d+_\\w+)" --repl "photo_\\1"

    # Actually rename (remove a "copy " prefix)
    python batch_rename.py D:/docs --pattern "copy (.*)" --repl "\\1" --apply
"""
import argparse
import os
import re


def main() -> int:
    ap = argparse.ArgumentParser(
        description="Batch rename files by regex pattern (dry-run by default)."
    )
    ap.add_argument("folder", help="Target folder")
    ap.add_argument("--pattern", required=True,
                    help="Regex matched against the filename (without extension)")
    ap.add_argument("--repl", required=True,
                    help="Replacement string; use \\1, \\2 ... for groups")
    ap.add_argument("--apply", action="store_true",
                    help="Actually rename (default is a safe dry-run)")
    args = ap.parse_args()

    if not os.path.isdir(args.folder):
        print(f"Not a directory: {args.folder}")
        return 1

    try:
        rx = re.compile(args.pattern)
    except re.error as e:
        print(f"Invalid regex: {e}")
        return 1

    renamed = 0
    for fn in sorted(os.listdir(args.folder)):
        fp = os.path.join(args.folder, fn)
        if not os.path.isfile(fp):
            continue
        base, ext = os.path.splitext(fn)
        new_base = rx.sub(args.repl, base)
        if new_base == base:
            continue
        new_fn = new_base + ext
        new_fp = os.path.join(args.folder, new_fn)
        flag = "RENAME" if args.apply else "would rename"
        print(f"{flag}: {fn} -> {new_fn}")
        if args.apply:
            if os.path.exists(new_fp):
                print(f"  SKIP (target exists): {new_fn}")
                continue
            os.rename(fp, new_fp)
            renamed += 1

    print(f"\n{'Renamed' if args.apply else 'Would rename'} {renamed} file(s).")
    if not args.apply:
        print("Add --apply to perform the renames for real.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
