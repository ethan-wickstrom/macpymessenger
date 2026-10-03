from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

import pytest

SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "check_release_version.py"


@pytest.mark.parametrize(
    ("metadata", "version", "exit_code", "message"),
    [
        (
            {"info": {"name": "macpymessenger"}, "releases": {"0.3.0": []}},
            "0.3.0",
            1,
            "already exists on PyPI",
        ),
        (
            {"info": {"name": "macpymessenger"}, "releases": {"0.3.0": []}},
            "0.4.0",
            0,
            "Refresh the snapshot",
        ),
        ({"info": {"name": "another-package"}, "releases": {}}, "0.4.0", 2, "different project"),
        ({"info": {"name": "macpymessenger"}}, "0.4.0", 2, "releases mapping"),
    ],
)
def test_release_version_preflight(
    tmp_path: Path,
    metadata: dict[str, object],
    version: str,
    exit_code: int,
    message: str,
) -> None:
    project = tmp_path / "pyproject.toml"
    project.write_text(f'[project]\nname = "macpymessenger"\nversion = "{version}"\n')
    snapshot = tmp_path / "pypi.json"
    snapshot.write_text(json.dumps(metadata))
    result = subprocess.run(  # noqa: S603
        [
            sys.executable,
            str(SCRIPT),
            "--pyproject",
            str(project),
            "--published-metadata",
            str(snapshot),
        ],
        cwd=tmp_path,
        capture_output=True,
        text=True,
        check=False,
    )
    assert result.returncode == exit_code
    assert message in (result.stdout if exit_code == 0 else result.stderr)
    assert project.read_text() == (f'[project]\nname = "macpymessenger"\nversion = "{version}"\n')
