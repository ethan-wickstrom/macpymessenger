import os

from jinja2 import Environment, FileSystemLoader

from macpymessenger.src.message_template import MessageTemplate


class TemplateManager:
    def __init__(self, template_dir='templates'):
        self.template_dir = template_dir
        self.templates = {}
        self.load_templates()

    def load_templates(self):
        for filename in os.listdir(self.template_dir):
            if filename.endswith('.txt'):
                template_id = os.path.splitext(filename)[0]
                with open(os.path.join(self.template_dir, filename), 'r') as file:
                    content = file.read()
                    self.create_template(template_id, content)

    def create_template(self, template_id, content, parent=None):
        if template_id in self.templates:
            raise ValueError(f"Template with ID '{template_id}' already exists.")
        template = MessageTemplate(template_id, content, parent)
        self.templates[template_id] = template

    def get_template(self, template_id):
        if template_id not in self.templates:
            raise ValueError(f"Template with ID '{template_id}' does not exist.")
        return self.templates[template_id]

    def update_template(self, template_id, new_content):
        template = self.get_template(template_id)
        template.update_content(new_content)

    def delete_template(self, template_id):
        if template_id not in self.templates:
            raise ValueError(f"Template with ID '{template_id}' does not exist.")
        del self.templates[template_id]

    def render_template(self, template_id, context):
        template = self.get_template(template_id)
        env = Environment(loader=FileSystemLoader('.'), autoescape=True)
        env.globals['include'] = self.include_template
        return template.render(**context)

    def include_template(self, template_id, **context):
        template = self.get_template(template_id)
        return template.render(**context)

    def compose_template(self, template_id, **context):
        template = self.get_template(template_id)
        rendered_content = template.render(**context)
        composed_template = MessageTemplate(f"{template_id}_composed", rendered_content)
        return composed_template