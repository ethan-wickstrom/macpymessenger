from __future__ import annotations

import subprocess
import sys
from pathlib import Path
from zipfile import ZipFile

PROJECT_ROOT = Path(__file__).resolve().parent.parent


def _build_wheel(destination: Path) -> Path:
    dist_dir = destination / "dist"
    dist_dir.mkdir()
    subprocess.run(
        [sys.executable, "-m", "build", "--wheel", "--outdir", str(dist_dir)],
        check=True,
        cwd=PROJECT_ROOT,
    )
    wheels = list(dist_dir.glob("macpymessenger-*.whl"))
    assert len(wheels) == 1
    return wheels[0]


def test_installed_wheel_exports_configuration(tmp_path: Path) -> None:
    wheel_path = _build_wheel(tmp_path)
    install_dir = tmp_path / "site-packages"
    install_dir.mkdir()
    with ZipFile(wheel_path) as archive:
        archive.extractall(install_dir)
    command = "\n".join(
        [
            "import sys",
            f"sys.path.insert(0, '{install_dir.as_posix()}')",
            "from macpymessenger import Configuration",
            "print(Configuration.__module__)",
        ]
    )
    result = subprocess.run(
        [sys.executable, "-c", command],
        check=True,
        capture_output=True,
        text=True,
        cwd=tmp_path,
    )
    assert result.stdout.strip() == "macpymessenger.configuration"
