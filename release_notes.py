"""Generate concise release notes from Git commit subjects."""

from __future__ import annotations

import argparse
import subprocess
from collections import defaultdict


def group_commits(subjects: list[str]) -> dict[str, list[str]]:
    groups: dict[str, list[str]] = defaultdict(list)
    for subject in subjects:
        if ":" in subject:
            kind, message = subject.split(":", 1)
            kind = kind.split("(", 1)[0].strip().lower()
            message = message.strip()
        else:
            kind, message = "other", subject.strip()
        groups[kind].append(message)
    return dict(groups)


def read_commits(start: str, end: str) -> list[str]:
    result = subprocess.run(
        ["git", "log", "--format=%s", f"{start}..{end}"],
        check=True,
        capture_output=True,
        text=True,
    )
    return [line for line in result.stdout.splitlines() if line.strip()]


def render(groups: dict[str, list[str]], title: str) -> str:
    labels = {"feat": "Features", "fix": "Fixes", "docs": "Documentation", "other": "Other"}
    lines = [f"# {title}", ""]
    for kind in ("feat", "fix", "docs", "other"):
        if kind not in groups:
            continue
        lines.extend([f"## {labels.get(kind, kind.title())}", ""])
        lines.extend(f"- {message}" for message in groups[kind])
        lines.append("")
    return "\n".join(lines).rstrip() + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate release notes from Git commits")
    parser.add_argument("start", help="starting Git ref")
    parser.add_argument("end", help="ending Git ref")
    parser.add_argument("--title", default="Release Notes", help="document title")
    args = parser.parse_args()
    print(render(group_commits(read_commits(args.start, args.end)), args.title), end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
