class MessageTemplate:
    def __init__(self, template_id, content):
        self.template_id = template_id
        self.content = content

    def update_content(self, new_content):
        self.content = new_content

    def __str__(self):
        return f"MessageTemplate(id={self.template_id}, content='{self.content}')"
