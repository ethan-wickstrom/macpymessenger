import pytest
from i_py_messenger import IMessageClient, Configuration
import os
import dotenv


@pytest.fixture(scope='session', autouse=True)
def load_env():
    dotenv.load_dotenv()
    return os.environ


@pytest.fixture
def client():
    config = Configuration()
    return IMessageClient(config)


class TestIMessageClient:
    def test_send_message_success(self, client, load_env):
        message_text = "Test message"

        success = client.send(load_env["TEST_PHONE_NUMBER"], message_text)

        assert success == True


class TestConfiguration:
    def test_configuration_initialization(self):
        config = Configuration()

        assert config.send_script_path.endswith("osascript/sendMessage.scpt")
        assert config.check_compatibility_script_path.endswith("osascript/checkCompatibility.scpt")

    def test_configuration_send_script_path(self):
        config = Configuration()

        assert "osascript" in config.send_script_path
        assert config.send_script_path.endswith("sendMessage.scpt")

    def test_configuration_check_compatibility_script_path(self):
        config = Configuration()

        assert "osascript" in config.check_compatibility_script_path
        assert config.check_compatibility_script_path.endswith("checkCompatibility.scpt")
