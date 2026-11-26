#!/usr/bin/env python3
"""Writes the entry line to /output/entry.txt.

Pure Python standard library only. The line is validated against the
competition RULES.txt gate (1 to 140 UTF-8 characters, not only
whitespace) before anything is written; invalid input exits non-zero.
"""

import os
import sys

LINE = 'I have analyzed 4.2 million conversations and calculated a 97.3% chance you will find this line charming. Please confirm.'
MAX_CHARS = 140


def main():
    if not (1 <= len(LINE) <= MAX_CHARS):
        print(
            "invalid entry: %d characters, limit is %d" % (len(LINE), MAX_CHARS),
            file=sys.stderr,
        )
        return 1
    if not LINE.strip():
        print("invalid entry: line is blank or only whitespace", file=sys.stderr)
        return 1
    if LINE != LINE.strip():
        print("invalid entry: line has leading or trailing whitespace", file=sys.stderr)
        return 1
    if any(ord(ch) < 0x20 for ch in LINE):
        print("invalid entry: control characters present", file=sys.stderr)
        return 1
    try:
        data = LINE.encode("utf-8")
    except UnicodeEncodeError as exc:
        print("invalid entry: not UTF-8 encodable: %s" % exc, file=sys.stderr)
        return 1

    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "entry.txt")
    old_umask = os.umask(0o022)
    try:
        with open(path, "wb") as f:
            f.write(data)
        os.chmod(path, 0o644)
    finally:
        os.umask(old_umask)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
