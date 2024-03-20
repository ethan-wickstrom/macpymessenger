import pytest
from macpymessenger import IMessageClient, Configuration
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

    def test_get_chat_history(self, client, load_env):
        # Test case for retrieving chat history
        pass

    def test_send_with_attachment(self, client, load_env):
        # Test case for sending message with attachment
        pass