# 🚀💬 macpymessenger

macpymessenger is a Python library that provides a simple interface for sending iMessages on macOS. It allows you to send text messages programmatically using the Messages app on your Mac.

## Features

| Feature                   | Status |
|---------------------------|--------|
| Send text messages        | ✅     |
| Check compatibility       | ❌     |
| Send images               | ❌     |
| Send attachments          | ❌     |
| Receive messages          | ❌     |
| Group messaging           | ❌     |
| Bulk messaging            | ❌     |
| Message history retrieval | ❌     |
| Message status retrieval  | ❌     |

## 🔑 Installation

You can install macpymessenger using pip:

```bash
pip install macpymessenger
```

## 🧑🏽‍💻 Usage

Here's a simple example of how to use macpymessenger to send a text message:

```python
from macpymessenger import IMessageClient, Configuration

config = Configuration()
client = IMessageClient(config)

phone_number = "1234567890"
message = "Hello, this is a test message sent using macpymessenger!"

success = client.send(phone_number, message)

if success:
    print("Message sent successfully!")
else:
    print("Failed to send the message.")
```

## ⚙️ Configuration

The `Configuration` class allows you to customize the paths to the AppleScript files used by macpymessenger. By default, it uses the following paths:

- `send_script_path`: `osascript/sendMessage.scpt`
- `check_compatibility_script_path`: `osascript/checkCompatibility.scpt`

You can modify these paths if needed by creating an instance of the `Configuration` class and setting the desired paths.

## 🧪 Testing

macpymessenger includes a test suite to ensure the functionality of the library. To run the tests, make sure you have the required dependencies installed and execute the following command:

```bash
python -m pytest test.py
```

The tests cover the following scenarios:
- Sending a message successfully
- Initializing the `Configuration` class
- Verifying the paths of the AppleScript files

## 📦 Project Structure

```
macpymessenger/
│
├── macpymessenger/
│   ├── __init__.py
│   ├── imessage_client.py
│   └── src/
│       ├── osascript/
│       │   └── sendMessage.scpt
│       ├── __init__.py
│       └── configuration.py
│
├── tests/
│   ├── __init__.py
│   ├── test_imessage_client.py
│   └── test_configuration.py
│
├── .github/
│   ├── workflows/
│   │   └── python-publish.yml
│   └── dependabot.yml
│
├── .env.template
├── .gitignore
├── LICENSE
├── README.md
├── requirements.txt
└── setup.py
```

## 📜 License

macpymessenger is licensed under the Apache License 2.0. See the [LICENSE](LICENSE) file for more information.

## 🤝 Contributing

Contributions to macpymessenger are welcome! If you find any issues or have suggestions for improvements, please open an issue or submit a pull request on the [GitHub repository](https://github.com/ethan-wickstrom/macpymessenger).

## 🙏 Acknowledgements

Originally forked from [Rolstenhouse/py-iMessage](https://github.com/Rolstenhouse/py-iMessage), macpymessenger was inspired by the need for a simple and intuitive way to send iMessages using Python on macOS. Special thanks to the developers of the libraries and tools used in this project.

## 📧 Contact

If you have any questions or inquiries, feel free to reach out to me:

- **Email:** e.t.wickstrom@wustl.edu
- **GitHub:** [ethan-wickstrom](https://github.com/ethan-wickstrom)

Thank you for using macpymessenger!