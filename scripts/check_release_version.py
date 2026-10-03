"""Reject a release version already present in a saved PyPI JSON response."""

from __future__ import annotations

import argparse
import json
import sys
import tomllib
from pathlib import Path


def main() -> int:
    """Check local metadata without network access or publication side effects."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--published-metadata", type=Path, required=True)
    parser.add_argument("--pyproject", type=Path, default=Path("pyproject.toml"))
    arguments = parser.parse_args()
    with arguments.pyproject.open("rb") as stream:
        project = tomllib.load(stream)["project"]
    metadata = json.loads(arguments.published_metadata.read_text(encoding="utf-8"))
    if metadata.get("info", {}).get("name") != project["name"]:
        sys.stderr.write("Published metadata belongs to a different project.\n")
        return 2
    releases = metadata.get("releases")
    if not isinstance(releases, dict):
        sys.stderr.write("Published metadata must include the releases mapping.\n")
        return 2
    version = project["version"]
    if version in releases:
        sys.stderr.write(
            f"Version {version} already exists on PyPI. Keep development changes Unreleased; "
            "choose a new version when preparing a release.\n"
        )
        return 1
    sys.stdout.write(
        f"Version {version} is absent from this PyPI snapshot. "
        "Refresh the snapshot before releasing; this does not verify release readiness.\n"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
