Testing
=======

macpymessenger includes a comprehensive test suite to ensure the reliability and stability of the library. In this section, we'll cover how to run the tests and interpret the results.

Running the Tests
-----------------

To run the macpymessenger test suite, follow these steps:

1. Make sure you have the necessary dependencies installed. You can install them using the following command:

   .. code-block:: bash

      pip install -r requirements.txt

2. Open a terminal and navigate to the project root directory.

3. Run the following command to execute the tests:

   .. code-block:: bash

      python -m pytest tests/

   This command will discover and run all the test cases defined in the `tests/` directory.

4. The test results will be displayed in the terminal, indicating the number of tests passed, failed, or skipped.

Interpreting Test Results
-------------------------

The test results provide valuable information about the health and functionality of macpymessenger. Here's how to interpret the test results:

- **Passed tests**: If a test case passes, it means the corresponding functionality is working as expected. The test suite will display a green dot (`.`) for each passed test.

- **Failed tests**: If a test case fails, it indicates that there is an issue with the corresponding functionality. The test suite will display a red `F` for each failed test and provide details about the failure, including the assertion that failed and the line of code where the failure occurred.

- **Skipped tests**: In some cases, certain test cases may be skipped due to specific conditions or configurations. Skipped tests are denoted by a yellow `s` in the test results.

If any tests fail, it's important to investigate the cause of the failure and fix the underlying issue. The test suite provides detailed information about each failure, including the traceback and the expected vs. actual values.

Writing Custom Tests
--------------------

In addition to the existing test cases, you can write your own custom tests to verify specific functionality or edge cases. To create a new test case:

1. Create a new Python file in the `tests/` directory with a name that starts with `test_`.

2. Import the necessary modules and dependencies.

3. Define test functions that use the `pytest` framework and make assertions about the expected behavior.

4. Run the test suite again to execute your new test cases.

Here's an example of a custom test case:

.. code-block:: python

   from macpymessenger import IMessageClient, Configuration

   def test_send_message_with_emoji():
       config = Configuration()
       client = IMessageClient(config)

       phone_number = "1234567890"
       message = "Hello 👋 from macpymessenger!"

       success = client.send(phone_number, message)

       assert success is True

This test case verifies that sending a message with an emoji works as expected.

By writing comprehensive tests and running them regularly, you can ensure the quality and reliability of your macpymessenger project.