Usage
=====

Using macpymessenger is straightforward and intuitive. In this section, we'll walk through the basic usage of the library and provide code examples to help you get started.

Sending Messages
----------------

To send an iMessage using macpymessenger, follow these steps:

1. Import the necessary classes:

   .. code-block:: python

      from macpymessenger import IMessageClient, Configuration

2. Create an instance of the `Configuration` class:

   .. code-block:: python

      config = Configuration()

3. Initialize the `IMessageClient` with the configuration:

   .. code-block:: python

      client = IMessageClient(config)

4. Use the `send` method to send a message:

   .. code-block:: python

      phone_number = "1234567890"
      message = "Hello, this is a test message sent using macpymessenger!"
      success = client.send(phone_number, message)

   The `send` method takes the recipient's phone number and the message content as arguments. It returns a boolean value indicating whether the message was sent successfully.

Managing Message Templates
--------------------------

macpymessenger allows you to create and manage message templates for convenient reuse. Here's how you can work with message templates:

1. Create a new message template:

   .. code-block:: python

      template_id = "greeting"
      content = "Hello, {name}! Welcome to macpymessenger."
      client.create_template(template_id, content)

2. Send a message using a template:

   .. code-block:: python

      phone_number = "1234567890"
      template_id = "greeting"
      client.send_template(phone_number, template_id)

3. Update an existing template:

   .. code-block:: python

      template_id = "greeting"
      new_content = "Hello, {name}! Welcome to the updated macpymessenger."
      client.update_template(template_id, new_content)

4. Delete a template:

   .. code-block:: python

      template_id = "greeting"
      client.delete_template(template_id)

These are just a few examples of what you can do with macpymessenger. The library provides additional features and customization options, which we'll explore in the following sections.

For more detailed information on the available methods and their parameters, please refer to the API reference documentation.