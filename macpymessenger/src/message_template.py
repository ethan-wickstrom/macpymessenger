from jinja2 import Environment, FileSystemLoader


class MessageTemplate:
    def __init__(self, template_id, content, parent=None):
        self.template_id = template_id
        self.content = content
        self.parent = parent

    def render(self, **context):
        env = Environment(loader=FileSystemLoader('.'), autoescape=True)
        template = env.from_string(self.content)
        if self.parent:
            parent_template = env.get_template(self.parent)
            template = parent_template.render(content=template.render(**context), **context)
        return template.render(**context)

    def update_content(self, new_content):
        self.content = new_content

    def __str__(self):
        return f"MessageTemplate(id={self.template_id}, content='{self.content}')"
