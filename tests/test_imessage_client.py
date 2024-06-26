import pytest
from macpymessenger import IMessageClient, Configuration
import os
import dotenv


@pytest.fixture(scope='session', autouse=True)
def load_env():
    dotenv.load_dotenv()
    return os.environ


@pytest.fixture
def client():
    config = Configuration()
    return IMessageClient(config)


class TestIMessageClient:
    def test_send_message_success(self, client, load_env):
        message_text = "Test message"

        success = client.send(load_env["TEST_PHONE_NUMBER"], message_text)

        assert success == True

    def test_send_bulk_success(self, client, load_env):
        phone_numbers = [
            load_env["TEST_PHONE_NUMBER_1"],
            load_env["TEST_PHONE_NUMBER_2"],
            load_env["TEST_PHONE_NUMBER_3"]
        ]
        message = "Bulk test message"

        successful_sends, failed_sends = client.send_bulk(phone_numbers, message)
        assert len(successful_sends) == 3
        assert len(failed_sends) == 0

    def test_create_and_send_template(self, client, load_env):
        template_id = "test_template"
        template_content = "Hello, {{ name }}! This is a test template."
        context = {"name": "John"}

        client.create_template(template_id, template_content)
        success = client.send_template(load_env["TEST_PHONE_NUMBER"], template_id, context)

        assert success == True

    def test_update_template(self, client, load_env):
        template_id = "test_template"
        original_content = "Hello, {{ name }}! This is a test template."
        updated_content = "Hello, {{ name }}! This is an updated test template."
        context = {"name": "John"}

        client.create_template(template_id, original_content)
        client.update_template(template_id, updated_content)
        success = client.send_template(load_env["TEST_PHONE_NUMBER"], template_id, context)

        assert success == True

    def test_delete_template(self, client):
        template_id = "test_template"
        template_content = "Hello, {{ name }}! This is a test template."

        client.create_template(template_id, template_content)
        client.delete_template(template_id)

        with pytest.raises(ValueError):
            client.send_template("1234567890", template_id, {})

    def test_render_template_with_context(self, client):
        template_id = "test_template"
        template_content = "Hello, {{ name }}! Your age is {{ age }}."
        context = {"name": "John", "age": 25}

        client.create_template(template_id, template_content)
        rendered_template = client.template_manager.render_template(template_id, context)

        assert rendered_template == "Hello, John! Your age is 25."

    def test_template_inheritance(self, client):
        base_template_id = "base_template"
        base_template_content = "<html><body>{% block content %}{% endblock %}</body></html>"
        child_template_id = "child_template"
        child_template_content = "{% extends 'base_template' %}{% block content %}<h1>Hello, {{ name }}!</h1>{% endblock %}"
        context = {"name": "John"}

        client.create_template(base_template_id, base_template_content)
        client.create_template(child_template_id, child_template_content, parent=base_template_id)
        rendered_template = client.template_manager.render_template(child_template_id, context)

        assert rendered_template == "<html><body><h1>Hello, John!</h1></body></html>"

    def test_template_include(self, client):
        header_template_id = "header_template"
        header_template_content = "<header>{{ title }}</header>"
        footer_template_id = "footer_template"
        footer_template_content = "<footer>{{ year }}</footer>"
        main_template_id = "main_template"
        main_template_content = "<html><body>{% include 'header_template' title='Welcome' %}{% include 'footer_template' year=2023 %}</body></html>"

        client.create_template(header_template_id, header_template_content)
        client.create_template(footer_template_id, footer_template_content)
        client.create_template(main_template_id, main_template_content)
        rendered_template = client.template_manager.render_template(main_template_id, {})

        assert rendered_template == "<html><body><header>Welcome</header><footer>2023</footer></body></html>"

    def test_get_chat_history(self, client, load_env):
        # Test case for retrieving chat history
        pass

    def test_send_with_attachment(self, client, load_env):
        # Test case for sending message with attachment
        pass