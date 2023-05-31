import pytest

from utils.Handlers.check_code_handler import check_code


class TelebotMock:
    def __init__(self):
        self.sent_messages = []

    def send_message(self, chat_id, text):
        self.sent_messages.append((chat_id, text))


def test_check_code_valid_code():
    telebot_instance = TelebotMock()

    message = type("Message", (object,), {"text": "/check_code print('Hello, world!')", "chat": type("Chat", (object,), {"id": "chat_id"})})
    check_code(message, telebot_instance)

    assert len(telebot_instance.sent_messages) == 1
    # Add assertions for the content of the first sent message, which should contain the result for valid code


def test_check_code_syntax_error():
    telebot_instance = TelebotMock()

    message = type("Message", (object,), {"text": "/check_code print('Hello, world!'", "chat": type("Chat", (object,), {"id": "chat_id"})})
    check_code(message, telebot_instance)

    assert len(telebot_instance.sent_messages) == 1
    # Add assertions for the content of the second sent message, which should contain the syntax error message


def test_check_code_pep8_errors():
    telebot_instance = TelebotMock()

    message = type("Message", (object,), {"text": "/check_code x = 5\nprint(x)", "chat": type("Chat", (object,), {"id": "chat_id"})})
    check_code(message, telebot_instance)

    assert len(telebot_instance.sent_messages) == 1
    # Add assertions for the content of the third sent message, which should contain the PEP-8 error messages


def test_check_code_no_errors():
    telebot_instance = TelebotMock()

    message = type("Message", (object,), {"text": "/check_code a = 1\nb = 2\nprint(a + b)", "chat": type("Chat", (object,), {"id": "chat_id"})})
    check_code(message, telebot_instance)

    assert len(telebot_instance.sent_messages) == 1
    # Add assertions for the content of the fourth sent message, which should indicate no syntax errors or PEP-8 errors


def test_check_code_empty_code():
    telebot_instance = TelebotMock()

    message = type("Message", (object,), {"text": "/check_code", "chat": type("Chat", (object,), {"id": "chat_id"})})
    check_code(message, telebot_instance)

    assert len(telebot_instance.sent_messages) == 1
    # Add assertions for the content of the fifth sent message, which should prompt the user to provide code


def test_check_code_comments_only():
    telebot_instance = TelebotMock()

    message = type("Message", (object,), {"text": "/check_code # This is a comment\n# Another comment", "chat": type("Chat", (object,), {"id": "chat_id"})})
    check_code(message, telebot_instance)

    assert len(telebot_instance.sent_messages) == 1
    # Add assertions for the content of the sixth sent message, which should indicate no syntax errors or PEP-8 errors


