import pytest
from py_imessage import IMessageClient, Message


@pytest.fixture
def imessage_client():
    client = IMessageClient()
    yield client
    client.close()


def test_check_compatibility(imessage_client: IMessageClient):
    phone_number = input("Enter a phone number to test compatibility: ")
    is_compatible = imessage_client.check_compatibility(phone_number)
    assert isinstance(is_compatible, bool)
    if is_compatible:
        print(f"{phone_number} is compatible with iMessage.")
    else:
        print(f"{phone_number} is not compatible with iMessage.")


def test_send_message(imessage_client):
    phone_number = input("Enter a phone number to send a message: ")
    message_text = "Test message from iPyMessenger"
    guid = imessage_client.send(phone_number, message_text)
    assert isinstance(guid, str)
    print(f"Message sent successfully. GUID: {guid}")


def test_message_status(imessage_client):
    guid = input("Enter the GUID of a sent message: ")
    message = imessage_client.status(guid)
    assert isinstance(message, Message)
    print(f"Message status:")
    print(f"  GUID: {message.guid}")
    print(f"  Date: {message.date}")
    print(f"  Date Read: {message.date_read}")
    print(f"  Date Delivered: {message.date_delivered}")


def test_send_and_check_status(imessage_client):
    phone_number = input("Enter a phone number to send a message and check status: ")
    message_text = "Test message from iPyMessenger"
    guid = imessage_client.send(phone_number, message_text)
    assert isinstance(guid, str)
    print(f"Message sent successfully. GUID: {guid}")

    message = imessage_client.status(guid)
    assert isinstance(message, Message)
    print(f"Message status:")
    print(f"  GUID: {message.guid}")
    print(f"  Date: {message.date}")
    print(f"  Date Read: {message.date_read}")
    print(f"  Date Delivered: {message.date_delivered}")
