Usage
=====

**macpymessenger keeps the main path small.** You create a client, send a message, and handle typed errors.

Send a message
--------------

**Create a client from the default configuration.**

.. code-block:: python

   from macpymessenger import Configuration, IMessageClient
   from macpymessenger.exceptions import MessageSendError

   client = IMessageClient(Configuration())

**Call ``send()`` with a recipient and a message.**

.. code-block:: python

   try:
       client.send("+15555555555", "Hello from macpymessenger!")
   except MessageSendError as error:
       print(f"Delivery failed: {error}")

``send()`` returns ``None`` when delivery succeeds.

Handle send errors
------------------

**The client raises typed exceptions instead of returning status flags.**

- ``MessageSendError`` means delivery failed or AppleScript could not run.
- ``InvalidDelayTypeError`` means ``delay_seconds`` was not an ``int``. ``bool`` is not accepted.
- ``NegativeDelayError`` means ``delay_seconds`` was less than zero.

Delay a message
---------------

**Pass ``delay_seconds`` to wait before sending.**

.. code-block:: python

   client.send("+15555555555", "See you in a minute.", delay_seconds=60)

The bundled AppleScript honors the delay. It waits first, then sends. If delivery fails, ``osascript`` exits non-zero and the client raises ``MessageSendError``.

Create a template
-----------------

**A template is a callable that returns a Python 3.14 t-string.**

.. code-block:: python

   client.create_template(
       "greeting",
       lambda name: t"Hello, {name}! Welcome to macpymessenger.",
   )

Jinja2 is not used. There is no ``templates/`` directory.

Send a template
---------------

**Pass the template identifier and a context dictionary.**

.. code-block:: python

   client.send_template("+15555555555", "greeting", {"name": "Ada"})

The call is equivalent to rendering the template and then calling ``send()``.

You can also delay a templated message:

.. code-block:: python

   client.send_template(
       "+15555555555",
       "greeting",
       {"name": "Ada"},
       delay_seconds=30,
   )

Update and delete templates
---------------------------

**Use the same identifier when you want to replace a template.**

.. code-block:: python

   client.update_template("greeting", lambda name: t"Hi {name}, welcome back.")

**Delete templates you no longer need.**

.. code-block:: python

   client.delete_template("greeting")

Missing identifiers raise ``TemplateNotFoundError``. Duplicate identifiers raise ``TemplateAlreadyExistsError``.

Keep template values as strings
-------------------------------

**Every interpolation must resolve to ``str``.**

.. code-block:: python

   client.create_template("status", lambda name, status: t"Hi {name}. Status: {status}.")
   client.send_template("+15555555555", "status", {"name": "Ada", "status": "ready"})

If ``status`` is an ``int`` or another non-string value, rendering raises ``TemplateTypeError``.

Missing context values are regular Python call errors. The callable receives the context as keyword arguments.

Use TemplateManager directly
----------------------------

**Use ``TemplateManager`` when you want rendering without a client.**

.. code-block:: python

   from macpymessenger import TemplateManager

   manager = TemplateManager()
   manager.create_template("welcome", lambda name: t"Welcome, {name}.")

   rendered = manager.compose_template("welcome", {"name": "Ada"})
   print(rendered.content)

``compose_template()`` returns ``RenderedTemplate``. ``render_template()`` returns only the rendered string.

Send to multiple recipients
---------------------------

**Use ``send_bulk()`` to send one message to many recipients.**

.. code-block:: python

   numbers = ["+15555555555", "+15555555556", "+15555555557"]
   successful, failed = client.send_bulk(numbers, "Reminder: meeting at 10 AM.")

``send_bulk()`` returns ``(successful, failed)``.

- ``successful`` contains recipients where ``send()`` completed.
- ``failed`` contains recipients where ``MessageSendError`` was raised.

Use the failed list to retry or log the result:

.. code-block:: python

   if failed:
       print(f"Could not send to: {failed}")

Experimental stubs
------------------

**Two methods exist, but they are not implemented yet.**

- ``get_chat_history(phone_number, limit=10)``
- ``send_with_attachment(phone_number, message, attachment_path)``

Both methods always raise ``NotImplementedError``.

.. code-block:: python

   client.get_chat_history("+15555555555")  # raises NotImplementedError

Do not use these methods in production code yet.
