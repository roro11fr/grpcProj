import re
import subprocess
import sys


def main() -> int:
    try:
        branch = subprocess.check_output(
            ["git", "rev-parse", "--abbrev-ref", "HEAD"],
            text=True,
        ).strip()
    except subprocess.CalledProcessError:
        print("❌ Cannot determine current git branch.")
        return 1

    pattern = r"^(feature|fix|chore)/TASK-\d+$"
    if not re.match(pattern, branch):
        print(
            "❌ Invalid branch name:",
            branch,
            "\n   Use: feature/TASK-123 (or fix/chore)",
        )
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
