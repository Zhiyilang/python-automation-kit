#!/usr/bin/env python3
"""Find duplicate files in one or more directories by content hash (SHA-256).

Report-only by default (safe). Use --delete to move the *extra* copies into a
backup folder instead of deleting them outright.

Zero dependencies: Python standard library only. Works on Windows / macOS / Linux.

Examples
--------
    # Just report duplicates in your Downloads folder
    python file_dedup.py "C:/Users/me/Downloads"

    # Scan two folders, ignore files smaller than 1 KB
    python file_dedup.py D:/photos E:/backup --min-size 1024

    # Move extra copies to ./duplicates_backup (originals kept)
    python file_dedup.py D:/photos --delete
"""
import argparse
import hashlib
import os
import shutil
import sys


def sha256(path: str, bufsize: int = 65536) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        while True:
            chunk = f.read(bufsize)
            if not chunk:
                break
            h.update(chunk)
    return h.hexdigest()


def iter_files(roots):
    for root in roots:
        if os.path.isfile(root):
            yield root
            continue
        for dirpath, _dirnames, filenames in os.walk(root):
            for fn in filenames:
                yield os.path.join(dirpath, fn)


def main() -> int:
    ap = argparse.ArgumentParser(
        description="Find duplicate files by content hash (report-only by default)."
    )
    ap.add_argument("paths", nargs="+", help="Directories or files to scan")
    ap.add_argument("--min-size", type=int, default=0,
                    help="Ignore files smaller than N bytes")
    ap.add_argument("--delete", action="store_true",
                    help="Move extra copies to ./duplicates_backup (keeps one original)")
    args = ap.parse_args()

    hashes: dict[str, list[str]] = {}
    errors = 0
    for fp in iter_files(args.paths):
        try:
            size = os.path.getsize(fp)
            if size < args.min_size:
                continue
            h = sha256(fp)
            hashes.setdefault(h, []).append(fp)
        except OSError as e:
            print(f"skip {fp}: {e}", file=sys.stderr)
            errors += 1

    dups = {h: ps for h, ps in hashes.items() if len(ps) > 1}
    if not dups:
        print("No duplicates found.")
        return 0

    total_wasted = 0
    backup_dir = os.path.join(os.getcwd(), "duplicates_backup")
    if args.delete:
        os.makedirs(backup_dir, exist_ok=True)

    for h, ps in dups.items():
        size = os.path.getsize(ps[0])
        total_wasted += size * (len(ps) - 1)
        print(f"\nDUPLICATE GROUP ({len(ps)} copies, {size} bytes each):")
        keep = ps[0]
        print(f"  KEEP   {keep}")
        for p in ps[1:]:
            print(f"  EXTRA  {p}")
            if args.delete:
                dest = os.path.join(backup_dir, os.path.basename(p))
                # avoid name clash
                base, ext = os.path.splitext(dest)
                i = 1
                while os.path.exists(dest):
                    dest = f"{base}_{i}{ext}"
                    i += 1
                shutil.move(p, dest)
                print(f"         -> moved to {dest}")

    print(f"\nTotal wasted space: {total_wasted} bytes across {len(dups)} groups.")
    if args.delete:
        print(f"Extra copies moved to: {backup_dir}")
    elif errors:
        print(f"(skipped {errors} unreadable files)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
