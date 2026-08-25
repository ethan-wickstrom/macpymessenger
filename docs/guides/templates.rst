.. meta::
   :description lang=en:
      Create reusable iMessage text with Python 3.14 t-string template
      functions and macpymessenger.

Use message templates
=====================

A template is a Python function that returns a Python 3.14 t-string. Register the
function once, then supply keyword values when you send.

Create and send a template
--------------------------

.. code-block:: python

   from macpymessenger import IMessageClient

   client = IMessageClient()
   client.create_template(
       "build-result",
       lambda project, result: t"{project} build: {result}",
   )

   client.send_template(
       "+15555550123",
       "build-result",
       {"project": "Example", "result": "passed"},
   )

The context keys become keyword arguments to the template function. Missing or
unexpected keys raise the normal ``TypeError`` for that function call. A
template with no arguments can omit the context:

.. code-block:: python

   client.create_template("ready", lambda: t"The report is ready.")
   client.send_template("+15555550123", "ready")

Keep interpolated results as strings
------------------------------------

Every value that reaches a t-string interpolation must be a ``str``. Context
values may use other types when the function converts them before interpolation
or uses them only for control flow.

.. code-block:: python

   client.create_template("count", lambda count: t"Count: {str(count)}")
   client.send_template(
       "+15555550123",
       "count",
       {"count": 3},
   )

Interpolating the integer directly as ``t"Count: {count}"`` raises
``TemplateTypeError``. Conversion markers such as ``!s`` do not bypass the type
check; convert inside the expression when conversion is intentional.

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

``render_template()`` returns the final message as a plain string.
``list_templates()`` returns a shallow copy, so changing the returned dictionary
does not change the manager.
