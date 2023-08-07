from unittest.mock import Mock, patch

from Handlers.documentation_handler import search_documentation


class TelebotMock:
    def __init__(self):
        self.sent_messages = []

    def send_message(self, chat_id, text):
        self.sent_messages.append((chat_id, text))

    def reply_to(self, message, text):
        self.sent_messages.append((message.chat.id, text))


def test_search_documentation_empty_query():
    telebot_instance = TelebotMock()
    message = Mock()
    message.text = "/documentation"
    search_documentation(message, telebot_instance)
    assert len(telebot_instance.sent_messages) == 1
    # Add assertion for the content of the sent message, which should contain the expected response for an empty query


def test_search_documentation_no_keyword():
    telebot_instance = TelebotMock()
    message = Mock()
    message.text = "/some_other_command some_function"
    search_documentation(message, telebot_instance)
    assert len(telebot_instance.sent_messages) == 1
    # Add assertion for the content of the sent message, which should contain the expected response for a query
    # without the "documentation" keyword


def test_search_documentation_valid_function():
    telebot_instance = TelebotMock()
    message = Mock()
    message.text = "/documentation some_function"
    search_documentation(message, telebot_instance)
    assert len(telebot_instance.sent_messages) == 1
    # Add assertion for the content of the sent message, which should contain the expected documentation string for
    # the valid function name


def test_search_documentation_nonexistent_function():
    telebot_instance = TelebotMock()
    message = Mock()
    message.text = "/documentation non_existent_function"
    search_documentation(message, telebot_instance)
    assert len(telebot_instance.sent_messages) == 1
    # Add assertion for the content of the sent message, which should contain the expected response for a
    # non-existent function name


def test_search_documentation_error_retrieving():
    telebot_instance = TelebotMock()
    message = Mock()
    message.text = "/documentation some_function"
    # Mock the pydoc.render_doc function to raise an exception
    with patch(
        "pydoc.render_doc", side_effect=Exception("Error retrieving documentation")
    ):
        search_documentation(message, telebot_instance)
    assert len(telebot_instance.sent_messages) == 1
    # Add assertion for the content of the sent message, which should contain the expected response for an error
    # during documentation retrieval
