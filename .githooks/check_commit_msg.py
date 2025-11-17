#!/usr/bin/env python3
import re
import sys
from pathlib import Path


def main(path: str) -> int:
    msg = Path(path).read_text(encoding="utf-8").strip()
    pattern = r"^(?:TASK-)?\d{3,4} - .+"
    if not re.match(pattern, msg):
        print(
            "Commit message must match one of:\n"
            "  123 - short description\n"
            "  TASK-123 - short description\n"
            "  (3–4 digits accepted)"
        )
        return 1
    return 0


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Missing commit message file path.")
        sys.exit(1)
    sys.exit(main(sys.argv[1]))
