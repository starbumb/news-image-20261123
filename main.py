#!/usr/bin/env python3
"""Entry program for the 23 November 2026 news-image bounty.

Copies the bundled poster (entry.png, rendered by draw.py) into the
output folder. Uses only the Python standard library, so it runs in
the grader sandbox with nothing installed. The destination is
$MAKEFUN_OUTPUT_DIR when that variable is set, otherwise /output.
"""
import os
import shutil


def main():
    src = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")
    dest_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"
    os.makedirs(dest_dir, exist_ok=True)
    shutil.copyfile(src, os.path.join(dest_dir, "entry.png"))


if __name__ == "__main__":
    main()
