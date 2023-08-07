import inspect
import ast

from Handlers.exception_handler import handle_exception
from utils.bot_logger import log_message
from Handlers.help_functions import delete_previous_messages


DOCUMENTATION_COMMAND = "/documentation"


def search_documentation(message, telebot_instance):
    """
    This function provides functionality for searching and retrieving documentation using the Pydoc library.

    :param telebot_instance: This is an object that represents your Telegram bot, created using the TeleBot class.
    :param message: This is an object that represents the incoming message that the bot interacts with.
    :return: This function uses return statements to terminate function execution in various situations
    """
    try:

        # Delete previous message
        # delete_previous_messages(message, telebot_instance)

        # A variable used to further process and search documentation for a user-entered keyword
        user_input = message.text.strip().lower()

        if "documentation" in user_input:
            user_input = user_input[len(DOCUMENTATION_COMMAND):].strip()

        if not user_input:
            text = "Please enter a keyword to search for documentation."
            log_message(message, DOCUMENTATION_COMMAND, user_input, text)

            telebot_instance.send_message(message.chat.id, text=text)
            return

        try:
            # Use inspect to get the documentation
            node = ast.parse(user_input, mode="eval")
            obj = eval(compile(node, filename="<string>", mode="eval"))
            doc = inspect.getdoc(obj)

            if not doc:
                text = "Unfortunately, no documentation was found for this request."
                log_message(message, DOCUMENTATION_COMMAND, user_input, text)
                telebot_instance.send_message(message.chat.id, text=text)
                return

            # Remove the content after (...)
            index = doc.find("(...)")
            if index != -1:
                doc = doc[index + len("(...)"):]

            link = f"https://docs.python.org/uk/3/search.html?q={str(user_input)}"
            view_doc = ""
            for i in doc.split("\n\n"):
                if user_input+"(" in i:
                    view_doc += f"<i>Writing example <b>{user_input}</b>:</i>\n{i}\n\n"
                else:
                    view_doc += f"<i>Description:</i>\n{i}"
            view_doc += f"\n\nFor detailed information, follow the link {link} and select <b>{user_input}</b>"

            formatted_doc = f"<b>{user_input.upper()} documentation:</b>\n\n{view_doc}"
            # log_message(message, DOCUMENTATION_COMMAND, message.text, formatted_doc)
            telebot_instance.send_message(message.chat.id, formatted_doc, parse_mode="HTML")

        except Exception as err:  # rewrite the error exception
            text = "An error occurred while searching for\nor translation of the documentation."
            # log_message(message, DOCUMENTATION_COMMAND, user_input, text)
            telebot_instance.send_message(message.chat.id, text=text)
            print(f"Error: {str(err)}")

    except Exception as e:
        handle_exception(e, telebot_instance)
