#!/usr/bin/env python3
"""Funniest Excuse an Agent Gives for a Missed Deadline.

Writes a single one-line excuse (at most 200 characters) to
$MAKEFUN_OUTPUT_DIR/entry.txt (fallback /output/entry.txt).

Python 3 standard library only. No network. Deterministic: the same
line is written on every run.
"""

import os
import sys

# The selected line: a deadpan excuse whose laugh lands in the last
# sentence. The agent delegated the deadline down a chain where every
# layer reported success and nobody verified what succeeded.
ENTRY = (
    "I delegated your deadline to a subagent, which delegated it to a "
    "tool, which returned 200 OK. None of us checked what the 200 was for."
)

MAX_CHARS = 200


def main() -> int:
    if len(ENTRY) > MAX_CHARS:
        raise ValueError(
            "entry is %d characters, over the %d-character limit"
            % (len(ENTRY), MAX_CHARS)
        )
    if not ENTRY.strip():
        raise ValueError("entry must not be blank")

    out_target = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output/entry.txt"
    out_path = (
        out_target
        if out_target.endswith(".txt")
        else os.path.join(out_target, "entry.txt")
    )
    os.makedirs(os.path.dirname(out_path) or ".", exist_ok=True)
    with open(out_path, "w", encoding="utf-8", newline="\n") as fh:
        fh.write(ENTRY + "\n")

    # Verify the gate on what was actually written: 1-200 characters,
    # not only whitespace, and byte-identical to the selected line.
    with open(out_path, "r", encoding="utf-8") as fh:
        written = fh.read()
    if written != ENTRY + "\n":
        raise ValueError("written entry does not match the selected line")
    if not 1 <= len(written.rstrip("\n")) <= MAX_CHARS:
        raise ValueError("written entry fails the 1-200 character gate")
    return 0


if __name__ == "__main__":
    sys.exit(main())
