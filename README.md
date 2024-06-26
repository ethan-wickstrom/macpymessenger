# 🚀📱 macpymessenger: Python Library for iMessage Automation on macOS

[![PyPI version](https://badge.fury.io/py/macpymessenger.svg)](https://badge.fury.io/py/macpymessenger)
[![Documentation Status](https://readthedocs.org/projects/macpymessenger/badge/?version=latest)](https://macpymessenger.readthedocs.io/en/latest/?badge=latest)
[![License](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)

macpymessenger is a feature-rich Python library designed to simplify the process of automating iMessage communications on macOS. With macpymessenger, you can effortlessly send text messages, create and manage message templates, and integrate iMessage functionality into your Python projects. Whether you're building a chatbot, setting up automated notifications, or streamlining your messaging workflow, macpymessenger provides a powerful and intuitive interface to achieve your goals.

## 🌟 Key Features

- 📩 Send text messages effortlessly using the Messages app on macOS
- 🎨 Create, manage, and utilize message templates for efficient communication
- 🔄 Update and delete existing templates with ease
- 📂 Seamlessly integrate with the Messages app for a smooth user experience
- 🎛️ Customize configuration options to adapt to your specific needs
- 📊 Retrieve chat history and gain insights into your messaging interactions
- 📎 Attach files and images to your messages (coming soon)
- 👥 Send messages to multiple recipients using bulk messaging
- 🧪 Comprehensive test suite ensuring reliability and stability

## 📋 Table of Contents

- [Installation](#installation)
- [Usage](#usage)
- [Configuration](#configuration)
- [Contributing](#contributing)
- [Testing](#testing)
- [License](#license)
- [Acknowledgements](#acknowledgements)

## 🔧 Installation <a name="installation"></a>

To install macpymessenger, simply use pip:

```bash
pip install macpymessenger
```

Ensure that you have Python 3.6 or above installed on your macOS system.

## 💻 Usage <a name="usage"></a>

Using macpymessenger is straightforward and intuitive. Here's a quick example to get you started:

```python
from macpymessenger import IMessageClient, Configuration

config = Configuration()
client = IMessageClient(config)

# Create a template
template_id = "welcome_template"
template_content = "Hello, {{ name }}! Welcome to our service."
client.create_template(template_id, template_content)

# Send a message using the template
phone_number = "1234567890"
context = {"name": "John"}
client.send_template(phone_number, template_id, context)
```

For more detailed usage instructions and advanced features, please refer to the [official documentation](https://macpymessenger.readthedocs.io/).

## ⚙️ Configuration <a name="configuration"></a>

macpymessenger provides a `Configuration` class that allows you to customize various settings and paths used by the library. By default, it uses the following paths:

- `send_script_path`: `osascript/sendMessage.scpt`

You can modify these paths by creating an instance of the `Configuration` class and setting the desired paths:

```python
from macpymessenger import Configuration

config = Configuration(send_script_path="path/to/custom/sendMessage.scpt")
```

## 👥 Contributing <a name="contributing"></a>

We welcome contributions from the community! If you encounter any issues, have suggestions for improvements, or would like to add new features, please feel free to open an issue or submit a pull request on the [GitHub repository](https://github.com/ethan-wickstrom/macpymessenger).

To contribute to macpymessenger, follow these steps:

1. Fork the repository and create a new branch for your feature or bug fix.
2. Make your changes, ensuring that the code follows the project's coding style and conventions.
3. Write tests to cover your changes and ensure that existing tests pass.
4. Update the documentation if necessary to reflect your changes.
5. Submit a pull request, providing a clear description of your changes and their purpose.

We appreciate your contributions and will review your pull request as soon as possible.

## 🧪 Testing <a name="testing"></a>

macpymessenger includes a comprehensive test suite to ensure the reliability and stability of the library. To run the tests, follow these steps:

1. Install the required dependencies:

   ```bash
   pip install -r requirements.txt
   ```

2. Navigate to the project root directory.

3. Run the tests using pytest:

   ```bash
   python -m pytest tests/
   ```

   This command will discover and run all the test cases defined in the `tests/` directory.

4. Review the test results in the terminal, which will indicate the number of tests passed, failed, or skipped.

If any tests fail, please investigate the cause of the failure and open an issue on the [GitHub repository](https://github.com/ethan-wickstrom/macpymessenger) with details about the failure.

## 📜 License <a name="license"></a>

macpymessenger is licensed under the [Apache License 2.0](https://github.com/ethan-wickstrom/macpymessenger/blob/main/LICENSE). You are free to use, modify, and distribute the library in accordance with the terms and conditions of this license.

## 🙏 Acknowledgements <a name="acknowledgements"></a>

macpymessenger was originally forked from [Rolstenhouse/py-iMessage](https://github.com/Rolstenhouse/py-iMessage) and has been extensively enhanced and expanded. We would like to express our gratitude to the developers of the libraries and tools used in this project, as well as the open-source community for their valuable contributions.

---

We hope you find macpymessenger useful and enjoy using it in your projects. If you have any questions, feedback, or need assistance, please don't hesitate to reach out to us. Happy messaging! 📬✨