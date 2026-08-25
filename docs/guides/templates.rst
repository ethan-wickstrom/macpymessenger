Use message templates
=====================

A template is a Python function that returns a Python 3.14 t-string. Register the
function once, then supply its values when you send.

Create and send a template
--------------------------

.. code-block:: python

   from macpymessenger import Configuration, IMessageClient

   client = IMessageClient(Configuration())
   client.create_template(
       "build-result",
       lambda project, result: t"{project} build: {result}",
   )

   client.send_template(
       "+15555550123",
       "build-result",
       {"project": "Example", "result": "passed"},
   )

The context keys become keyword arguments to the template function. If a key is
missing or unexpected, Python raises the normal ``TypeError`` for that function
call. A template with no arguments can omit the context:

.. code-block:: python

   client.create_template("ready", lambda: t"The report is ready.")
   client.send_template("+15555550123", "ready")

Keep every value a string
-------------------------

Every interpolated value must already be a ``str``. This keeps message output
predictable.

.. code-block:: python

   client.create_template("count", lambda count: t"Count: {count}")
   client.send_template(
       "+15555550123",
       "count",
       {"count": "3"},  # Use a string, not the integer 3.
   )

A non-string interpolation raises ``TemplateTypeError``. Conversions and format
specifications run only after this check.

Manage registered templates
----------------------------

.. code-block:: python

   client.update_template("ready", lambda: t"Your report is ready.")
   client.delete_template("ready")

Creating the same identifier twice raises ``TemplateAlreadyExistsError``.
Updating, deleting, or rendering an unknown identifier raises
``TemplateNotFoundError``.

Render without sending
----------------------

Use ``TemplateManager`` when you only need template storage and rendering:

.. code-block:: python

   from macpymessenger import TemplateManager

   manager = TemplateManager()
   manager.create_template("welcome", lambda name: t"Welcome, {name}.")

   message = manager.render_template("welcome", {"name": "Ada"})
   registered = manager.list_templates()

``render_template()`` returns a string. ``compose_template()`` returns a
``RenderedTemplate`` with the identifier and content. ``list_templates()``
returns a shallow copy, so changing the returned dictionary does not change the
manager.
