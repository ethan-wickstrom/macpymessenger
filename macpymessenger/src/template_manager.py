import os
from typing import Dict, Optional
from jinja2 import Environment, FileSystemLoader, Template
from .message_template import MessageTemplate
from .exceptions import TemplateNotFoundError, TemplateAlreadyExistsError


class TemplateManager:
    """Manages message templates for the macpymessenger library."""

    def __init__(self, template_dir: str = 'templates'):
        """
        Initialize the TemplateManager.

        Args:
            template_dir (str): The directory containing template files.
        """
        self.template_dir = template_dir
        self.templates: Dict[str, MessageTemplate] = {}
        self.env = Environment(loader=FileSystemLoader('.'), autoescape=True)
        self.env.globals['include'] = self.include_template
        self.load_templates()

    def load_templates(self) -> None:
        """Load all templates from the template directory."""
        for filename in os.listdir(self.template_dir):
            if filename.endswith('.txt'):
                template_id = os.path.splitext(filename)[0]
                with open(os.path.join(self.template_dir, filename), 'r') as file:
                    content = file.read()
                    self.create_template(template_id, content)

    def create_template(self, template_id: str, content: str, parent: Optional[str] = None) -> None:
        """
        Create a new message template.

        Args:
            template_id (str): The ID of the template.
            content (str): The content of the template.
            parent (Optional[str]): The ID of the parent template, if any.

        Raises:
            TemplateAlreadyExistsError: If a template with the given ID already exists.
        """
        if template_id in self.templates:
            raise TemplateAlreadyExistsError(f"Template with ID '{template_id}' already exists.")
        template = MessageTemplate(template_id, content, parent)
        self.templates[template_id] = template

    def get_template(self, template_id: str) -> MessageTemplate:
        """
        Retrieve a template by its ID.

        Args:
            template_id (str): The ID of the template to retrieve.

        Returns:
            MessageTemplate: The requested template.

        Raises:
            TemplateNotFoundError: If the template with the given ID does not exist.
        """
        if template_id not in self.templates:
            raise TemplateNotFoundError(f"Template with ID '{template_id}' does not exist.")
        return self.templates[template_id]

    def update_template(self, template_id: str, new_content: str) -> None:
        """
        Update an existing template.

        Args:
            template_id (str): The ID of the template to update.
            new_content (str): The new content for the template.

        Raises:
            TemplateNotFoundError: If the template with the given ID does not exist.
        """
        template = self.get_template(template_id)
        template.update_content(new_content)

    def delete_template(self, template_id: str) -> None:
        """
        Delete a template.

        Args:
            template_id (str): The ID of the template to delete.

        Raises:
            TemplateNotFoundError: If the template with the given ID does not exist.
        """
        if template_id not in self.templates:
            raise TemplateNotFoundError(f"Template with ID '{template_id}' does not exist.")
        del self.templates[template_id]

    def render_template(self, template_id: str, context: dict) -> str:
        """
        Render a template with the given context.

        Args:
            template_id (str): The ID of the template to render.
            context (dict): The context data for rendering the template.

        Returns:
            str: The rendered template content.
        """
        template = self.get_template(template_id)
        return template.render(**context)

    def include_template(self, template_id: str, **context) -> str:
        """
        Include a template within another template.

        Args:
            template_id (str): The ID of the template to include.
            **context: The context data for rendering the included template.

        Returns:
            str: The rendered content of the included template.
        """
        template = self.get_template(template_id)
        return template.render(**context)

    def compose_template(self, template_id: str, **context) -> MessageTemplate:
        """
        Compose a new template by rendering an existing template with context.

        Args:
            template_id (str): The ID of the template to compose.
            **context: The context data for rendering the template.

        Returns:
            MessageTemplate: A new MessageTemplate with the rendered content.
        """
        template = self.get_template(template_id)
        rendered_content = template.render(**context)
        return MessageTemplate(f"{template_id}_composed", rendered_content)
