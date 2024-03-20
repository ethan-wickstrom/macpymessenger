from i_py_messenger import IMessageClient, Configuration


def test_send_message(client):
    phone_number = input("Enter a phone number to send a message: ")
    message_text = "Test message from iPyMessenger"
    success = client.send(phone_number, message_text)
    if success:
        print("Message sent successfully.")
    else:
        print("Failed to send message.")


def test_check_compatibility(client):
    phone_number = input("Enter a phone number to test compatibility: ")
    is_compatible = client.check_compatibility(phone_number)
    if is_compatible:
        print(f"{phone_number} is compatible with iMessage.")
    else:
        print(f"{phone_number} is not compatible with iMessage.")


def run_tests():
    config = Configuration()
    client = IMessageClient(config)

    print("Running send message test...")
    test_send_message(client)

    print("\nRunning compatibility test...")
    test_check_compatibility(client)

    client.close()


if __name__ == "__main__":
    run_tests()