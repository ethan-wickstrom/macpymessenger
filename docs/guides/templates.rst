.. meta::
   :description lang=en:
      Create reusable iMessage text with Python 3.14 t-string template
      functions, conversions, and format specifications.

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

Use normal Python conversion and formatting
-------------------------------------------

Interpolated values use Python's normal conversion and format protocols. Strings,
integers, floats, and domain objects with ``__format__`` support can be rendered
directly:

.. code-block:: python

   client.create_template(
       "timing",
       lambda count, duration: t"Processed {count} items in {duration:.2f}s",
   )
   client.send_template(
       "+15555550123",
       "timing",
       {"count": 3, "duration": 1.234},
   )

Conversions such as ``!s`` and ``!r`` and format specifications such as
``:.2f`` behave as they do in f-strings. Exceptions raised by a value's
conversion or ``__format__`` implementation propagate normally.

Use context for control flow
----------------------------

The template function is ordinary Python. It can branch, compute values, or
choose which t-string to return:

.. code-block:: python

   def build_status(project: str, passed: bool):
       if passed:
           return t"{project} passed"
       return t"{project} failed"


   client.create_template("build-status", build_status)

A false-valued mapping is still a valid context. Only ``None`` means no context
was supplied.

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
