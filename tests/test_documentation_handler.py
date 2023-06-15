import pytest
from telebot.types import Message

from Handlers.documentation_handler import search_documentation


class MockTeleBot:
    def __init__(self):
        self.replied_messages = []
        self.sent_messages = []

    def reply_to(self, message, reply_text):
        self.replied_messages.append((message, reply_text))

    def send_message(self, chat_id, text, parse_mode=None):
        self.sent_messages.append((chat_id, text, parse_mode))


@pytest.fixture
def telebot_instance():
    return MockTeleBot()


def test_search_documentation(telebot_instance):
    message = Message()
    message.text = "/documentation str"

    search_documentation(message, telebot_instance)

    # Check if a reply message was sent
    assert len(telebot_instance.replied_messages) == 1
    assert telebot_instance.replied_messages[0] == (
        message,
        "Please enter a keyword to search",
    )

    # Check if a message was sent
    assert len(telebot_instance.sent_messages) == 0

    # Update the message text to search for valid documentation
    message.text = "/documentation valid_function"

    search_documentation(message, telebot_instance)

    # Check if no reply message was sent
    assert len(telebot_instance.replied_messages) == 1

    # Check if a message was sent with the formatted documentation
    assert len(telebot_instance.sent_messages) == 1
    assert telebot_instance.sent_messages[0][0] == message.chat.id
    assert (
        "<b>valid_function Documentation:</b>" in telebot_instance.sent_messages[0][1]
    )

    # Add more test cases as needed


if __name__ == "__main__":
    pytest.main()
