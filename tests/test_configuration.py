from pathlib import Path

import pytest

from macpymessenger.configuration import Configuration
from macpymessenger.exceptions import ScriptNotFoundError


def test_configuration_defaults_to_packaged_script() -> None:
    configuration = Configuration()
    assert configuration.send_script_path.name == "sendMessage.scpt"
    assert configuration.send_script_path.exists()


def test_configuration_uses_custom_script(tmp_path: Path) -> None:
    script_path = tmp_path / "custom.scpt"
    script_path.write_text("-- mock script", encoding="utf-8")
    configuration = Configuration(script_path)
    assert configuration.send_script_path == script_path


def test_configuration_raises_for_missing_script(tmp_path: Path) -> None:
    missing_path = tmp_path / "missing.scpt"
    with pytest.raises(ScriptNotFoundError):
        Configuration(missing_path)
