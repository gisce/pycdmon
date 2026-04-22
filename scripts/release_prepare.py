from __future__ import annotations

import re
import sys
from pathlib import Path


def bump_pyproject(version: str) -> None:
    path = Path("pyproject.toml")
    text = path.read_text()
    updated = re.sub(
        r'^version = ".*"$',
        f'version = "{version}"',
        text,
        count=1,
        flags=re.MULTILINE,
    )
    if text == updated:
        raise SystemExit("Could not update version in pyproject.toml")
    path.write_text(updated)


def main() -> int:
    if len(sys.argv) != 2:
        raise SystemExit("Usage: release_prepare.py <version>")
    bump_pyproject(sys.argv[1])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
