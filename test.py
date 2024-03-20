from i_py_messenger import IMessageClient, Configuration
from dotenv import dotenv_values


def test_send_message(client, phone_number, message_text):
    success = client.send(phone_number, message_text)
    if success:
        print("Message sent successfully.")
    else:
        print("Failed to send message.")


def test_check_compatibility(client, phone_number):
    is_compatible = client.check_compatibility(phone_number)
    if is_compatible:
        print(f"{phone_number} is compatible with iMessage.")
    else:
        print(f"{phone_number} is not compatible with iMessage.")


def test_get_most_recently_sent_text(client):
    most_recent_text = client.get_most_recently_sent_text()
    if most_recent_text:
        print(f"Most recently sent text: {most_recent_text}")
    else:
        print("No recently sent text found.")


def test_get_messages_for_phone_number(client):
    phone_number = input("Enter a phone number to retrieve messages: ")
    messages = client.get_messages_for_phone_number(phone_number)
    if messages:
        print(f"Messages for {phone_number}:")
        for message in messages:
            print(f"- {message.date}: {message.guid}")
    else:
        print(f"No messages found for {phone_number}.")


def run_tests():
    os_password = dotenv_values().get("OS_PASSWORD")
    test_phone_number = dotenv_values().get("TEST_PHONE_NUMBER")

    config = Configuration(
        os_password=os_password,
    )
    client = IMessageClient(config)

    print("Running send message test...")
    test_send_message(client, test_phone_number, "Test message from i_py_messenger.")

    print("\nRunning compatibility test...")
    test_check_compatibility(client, test_phone_number)

    print("\nRunning get most recently sent text test...")
    test_get_most_recently_sent_text(client)

    print("\nRunning get messages for phone number test...")
    test_get_messages_for_phone_number(client)

    client.close()


if __name__ == "__main__":
    run_tests()
