#!/usr/bin/env python3
"""make.fun bounty entry: 'Sum up 22 November's world news in one image'.

Writes the bundled poster (entry.png, next to this file) to
/output/entry.png. No network, no randomness: every run writes
exactly the same bytes.
"""
import shutil
from pathlib import Path

def main() -> None:
    src = Path(__file__).resolve().parent / "entry.png"
    dst = Path("/output/entry.png")
    dst.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(src, dst)

if __name__ == "__main__":
    main()
