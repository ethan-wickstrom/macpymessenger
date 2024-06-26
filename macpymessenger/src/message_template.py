from typing import Optional
from jinja2 import Environment, FileSystemLoader, Template, TemplateError


class MessageTemplate:
    """Represents a message template with optional inheritance."""

    def __init__(self, template_id: str, content: str, parent: Optional[str] = None):
        """
        Initialize a MessageTemplate.

        Args:
            template_id (str): The unique identifier for this template.
            content (str): The template content.
            parent (Optional[str]): The ID of the parent template, if any.
        """
        self.template_id = template_id
        self.content = content
        self.parent = parent
        self.env = Environment(loader=FileSystemLoader('.'), autoescape=True)
        self.template = self.env.from_string(content)

    def update_content(self, new_content: str) -> None:
        """
        Update the content of the template.

        Args:
            new_content (str): The new content for the template.
        """
        self.content = new_content
        self.template = self.env.from_string(new_content)

    def render(self, **context) -> str:
        """
        Render the template with the given context.

        Args:
            **context: The context data for rendering the template.

        Returns:
            str: The rendered template content.

        Raises:
            TemplateError: If an error occurs during rendering.
        """
        try:
            return self.template.render(**context)
        except TemplateError as e:
            raise TemplateError(f"Error rendering template '{self.template_id}': {str(e)}")

    def __str__(self) -> str:
        """Return a string representation of the MessageTemplate."""
        return f"MessageTemplate(template_id='{self.template_id}', content='{self.content}')"

    def __repr__(self) -> str:
        """Return a detailed string representation of the MessageTemplate."""
        return self.__str__()
