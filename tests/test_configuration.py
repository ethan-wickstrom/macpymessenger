from macpymessenger.src.configuration import Configuration


class TestConfiguration:
    def test_configuration_initialization(self):
        config = Configuration()

        assert config.send_script_path.endswith("osascript/sendMessage.scpt")

    def test_configuration_send_script_path(self):
        config = Configuration()

        assert "osascript" in config.send_script_path
        assert config.send_script_path.endswith("sendMessage.scpt")
