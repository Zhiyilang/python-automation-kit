#!/usr/bin/env python3
"""Print or export a directory tree with human-readable file sizes.

Zero dependencies: Python standard library only.

Examples
--------
    # Show tree of the current folder (2 levels deep)
    python folder_tree.py . --max-depth 2

    # Export the tree of D:/project to a file
    python folder_tree.py D:/project --out tree.txt
"""
import argparse
import os


def human(n: int) -> str:
    for unit in ["B", "KB", "MB", "GB", "TB"]:
        if n < 1024:
            return f"{n:.1f}{unit}" if unit != "B" else f"{n}B"
        n /= 1024
    return f"{n:.1f}PB"


def walk(root: str, prefix: str = "", lines=None, max_depth=None, depth: int = 0):
    if lines is None:
        lines = []
    if max_depth is not None and depth > max_depth:
        return lines
    try:
        entries = sorted(os.listdir(root))
    except OSError:
        return lines
    dirs = [e for e in entries if os.path.isdir(os.path.join(root, e))]
    files = [e for e in entries if os.path.isfile(os.path.join(root, e))]
    items = dirs + files
    for i, name in enumerate(items):
        last = (i == len(items) - 1)
        conn = "└── " if last else "├── "
        fp = os.path.join(root, name)
        if os.path.isdir(fp):
            lines.append(f"{prefix}{conn}{name}/")
            ext = "    " if last else "│   "
            walk(fp, prefix + ext, lines, max_depth, depth + 1)
        else:
            try:
                sz = os.path.getsize(fp)
            except OSError:
                sz = 0
            lines.append(f"{prefix}{conn}{name} ({human(sz)})")
    return lines


def main() -> int:
    ap = argparse.ArgumentParser(description="Directory tree with file sizes.")
    ap.add_argument("root", nargs="?", default=".", help="Root directory")
    ap.add_argument("--max-depth", type=int, default=None, help="Limit recursion depth")
    ap.add_argument("--out", default=None, help="Write to file instead of stdout")
    args = ap.parse_args()

    if not os.path.isdir(args.root):
        print(f"Not a directory: {args.root}")
        return 1

    lines = walk(args.root, max_depth=args.max_depth)
    out = "\n".join(lines)
    if args.out:
        with open(args.out, "w", encoding="utf-8") as f:
            f.write(out + "\n")
        print(f"Wrote tree to {args.out}")
    else:
        print(out)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
