.. meta::
   :description lang=en:
      API reference for registering and rendering Python 3.14 t-string message
      templates with macpymessenger.

Template API
============

TemplateManager
---------------

``TemplateManager`` stores callable t-string factories. ``render_template()``
returns the final message as a plain ``str``. No wrapper object or template-file
format sits between rendering and sending.

.. autoclass:: macpymessenger.TemplateManager
   :members: create_template, update_template, delete_template, render_template, list_templates
   :no-private-members:
   :no-special-members:
