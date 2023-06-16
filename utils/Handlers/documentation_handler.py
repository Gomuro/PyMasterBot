import inspect
import ast
import builtins

# from utils.bot_logger import log_message
from utils.Handlers.help_functions import delete_previous_messages

DOCUMENTATION_COMMAND = "/documentation"


def search_documentation(message, telebot_instance):
    """
    This function provides functionality for searching and retrieving documentation using the Pydoc library.

    :param telebot_instance: This is an object that represents your Telegram bot, created using the TeleBot class.
    :param message: This is an object that represents the incoming message that the bot interacts with.
    :return: This function uses return statements to terminate function execution in various situations
    """

    delete_previous_messages(message, telebot_instance)

    user_input = message.text.strip()

    if "documentation" in user_input:
        user_input = user_input[len(DOCUMENTATION_COMMAND):].strip()

    if not user_input:
        text = "Будь ласка, введіть ключове слово для пошуку документації."
        # log_message(message, DOCUMENTATION_COMMAND, user_input, text)
        telebot_instance.send_message(message.chat.id, text=text)
        return

    try:
        # Use inspect to get the documentation
        node = ast.parse(user_input, mode="eval")
        obj = eval(compile(node, filename="<string>", mode="eval"))
        doc = inspect.getdoc(obj)

        if not doc:
            text = "На жаль, не знайдено документації для даного запиту."
            # log_message(message, DOCUMENTATION_COMMAND, user_input, text)
            telebot_instance.send_message(message.chat.id, text=text)
            return

        if user_input in builtins.__dict__:
            function = getattr(builtins, user_input)
            docstring = function.__doc__
            if docstring:
                telebot_instance.send_message(message.chat.id, f"<b>Function: {user_input}</b>\n\n<i>Description: \n"
                                                               f"   {docstring}</i>", parse_mode="HTML")

    except Exception as err:
        text = "Виникла помилка при пошуку\n\nабо перекладі документації."
        # log_message(message, DOCUMENTATION_COMMAND, message.text, formatted_doc)
        telebot_instance.send_message(message.chat.id, text=text)
        print(f"Error: {str(err)}")
