from macpymessenger.src.message_template import MessageTemplate


class TemplateManager:
    def __init__(self):
        self.templates = {}

    def create_template(self, template_id, content):
        if template_id in self.templates:
            raise ValueError(f"Template with ID '{template_id}' already exists.")
        template = MessageTemplate(template_id, content)
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