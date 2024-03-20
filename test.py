from i_py_messenger import IMessageClient, Configuration
from dotenv import dotenv_values


def test_send_message(client: IMessageClient, phone_number, message_text):
    success = client.send(phone_number, message_text)
    if success:
        print("Message sent successfully.")
    else:
        print("Failed to send message.")


def test_check_compatibility(client: IMessageClient, phone_number):
    is_compatible = client.check_compatibility(phone_number)
    if is_compatible:
        print(f"{phone_number} is compatible with iMessage.")
    else:
        print(f"{phone_number} is not compatible with iMessage.")


def run_tests():
    test_phone_number = dotenv_values().get("TEST_PHONE_NUMBER")

    config = Configuration()
    client: IMessageClient = IMessageClient(config)

    print("Running send message test...")
    test_send_message(client, test_phone_number, "Test message from i_py_messenger.")

    print("\nRunning compatibility test...")
    test_check_compatibility(client, test_phone_number)


if __name__ == "__main__":
    run_tests()
