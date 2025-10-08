Usage
=====

**macpymessenger provides a simple API for sending iMessages and managing templates.**

This guide covers sending messages, creating templates, and handling errors.

Send a message
--------------

**Import the required classes:**

.. code-block:: python

   from macpymessenger import IMessageClient, Configuration
   from macpymessenger.exceptions import MessageSendError

**Create a configuration and client:**

.. code-block:: python

   config = Configuration()
   client = IMessageClient(config)

**Send a message:**

.. code-block:: python

   phone_number = "+15555555555"
   message = "Hello from macpymessenger!"
   
   try:
       client.send(phone_number, message)
   except MessageSendError as error:
       print(f"Delivery failed: {error}")

**The `send` method raises exceptions on failure:**

- `MessageSendError` — delivery failed
- `ValueError` — invalid `delay_seconds` parameter (negative values are not allowed)

**Success returns `None`.** No boolean return values.

Create and use templates
------------------------

**Templates let you reuse message patterns with variable substitution.**

Create a template:

.. code-block:: python

   template_id = "greeting"
   template_factory = lambda name: t"Hello, {name}! Welcome to macpymessenger."
   client.create_template(template_id, template_factory)

**Send a message using the template:**

.. code-block:: python

   phone_number = "+15555555555"
   client.send_template(phone_number, "greeting", {"name": "Ada"})

**Templates rely on callables that return t-strings.** Jinja2 is no longer used.

.. code-block:: python

   def premium_greeting(name: str, premium: str) -> Template:
       return t"Hello, {name}! {premium}"

   client.create_template("premium_greeting", premium_greeting)

**Update an existing template:**

.. code-block:: python

   client.update_template("greeting", lambda name: t"Hi {name}, welcome!")

**Delete a template:**

.. code-block:: python

   client.delete_template("greeting")

**Provide all variables in the context dictionary.** Missing values trigger `TypeError` because callables receive keyword arguments and forward them to t-strings.

**Return only strings from template callables.** If any interpolation resolves to a non-string value, the manager raises `TemplateTypeError`.

List all templates
------------------

**Get a dictionary of all registered template callables:**

.. code-block:: python

   factories = manager.list_templates()
   
   for identifier, factory in factories.items():
       print(f"{identifier}: {factory.__name__}")

**The returned dictionary is a shallow copy.** Modifying it does not affect the manager's internal state.

Send to multiple recipients
---------------------------

**The `send_bulk` method sends the same message to multiple phone numbers.**

.. code-block:: python

   numbers = ["+15551234567", "+15557654321"]
   successful, failed = client.send_bulk(numbers, "Reminder: meeting at 10 AM.")

**The method returns two lists:**

- `successful` — phone numbers where delivery succeeded
- `failed` — phone numbers where delivery failed

**Use the failed list to retry or log errors:**

.. code-block:: python

   if failed:
       print(f"Failed deliveries: {failed}")
       # Retry logic or alert

Experimental features
---------------------

**Two methods are defined but not yet implemented:**

- `get_chat_history` — for retrieving message history
- `send_with_attachment` — for sending files with messages

**Both methods raise `NotImplementedError` when called:**

.. code-block:: python

   # This will raise NotImplementedError
   client.get_chat_history("+15555555555")

**These methods exist to stabilize the API signature.** Do not call them in production code until they are fully implemented in a future release.
