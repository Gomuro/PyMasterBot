import pytest

from Handlers.callback_query_handler import callback_query_handler


@pytest.fixture
def telebot_instance(mocker):
    return mocker.Mock()


@pytest.fixture
def inline_keyboard(mocker):
    return mocker.Mock()


def test_help_command(mocker):
    telebot_instance = mocker.Mock()
    inline_keyboard = mocker.Mock()
    call = mocker.Mock(data="/help")

    callback_query_handler(call, telebot_instance, inline_keyboard)

    telebot_instance.answer_callback_query.assert_called_once_with(
        callback_query_id=call.id
    )
    telebot_instance.send_message.assert_called_once_with(
        chat_id=call.message.chat.id,
        text="I can help you with these commands:\n"
        "/help - help\n"
        "/check_code - syntax check\n"
        "/documentation - documentation",
        reply_markup=inline_keyboard.get_keyboard(),
    )


def test_check_code_command(mocker):
    telebot_instance = mocker.Mock()
    inline_keyboard = mocker.Mock()
    call = mocker.Mock(data="/check_code")

    callback_query_handler(call, telebot_instance, inline_keyboard)

    telebot_instance.answer_callback_query.assert_called_once_with(
        callback_query_id=call.id
    )
    telebot_instance.send_message.assert_called_once_with(
        chat_id=call.message.chat.id,
        text="Send the code you want to check.",
        reply_markup=inline_keyboard.get_keyboard(),
    )


def test_documentation_command(mocker):
    telebot_instance = mocker.Mock()
    inline_keyboard = mocker.Mock()
    call = mocker.Mock(data="/documentation")

    callback_query_handler(call, telebot_instance, inline_keyboard)

    telebot_instance.answer_callback_query.assert_called_once_with(
        callback_query_id=call.id
    )
    telebot_instance.send_message.assert_called_once_with(
        chat_id=call.message.chat.id,
        text="Enter the name of the module, function, or class: ",
        reply_markup=inline_keyboard.get_keyboard(),
    )


def test_invalid_command(mocker):
    telebot_instance = mocker.Mock()
    inline_keyboard = mocker.Mock()
    call = mocker.Mock(data="/invalid")

    callback_query_handler(call, telebot_instance, inline_keyboard)

    telebot_instance.answer_callback_query.assert_called_once_with(
        callback_query_id=call.id, text="This command does not exist!"
    )
