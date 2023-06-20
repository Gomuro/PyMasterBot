import inspect
import ast
import webbrowser


# from utils.bot_logger import log_message
from utils.Handlers.help_functions import delete_previous_messages

HELP_COMMAND = "/help"


def help_request_handler(message, telebot_instance):
    """
    This function provides responses to user requests.

    :param telebot_instance: This is an object that represents your Telegram bot, created using the TeleBot class.
    :param message: This is an object that represents the incoming message that the bot interacts with.
    :return: This function uses return statements to terminate function execution in various situations
    """
    user_input = message.text.strip()

    if "help" in user_input:
        user_input = user_input[len(HELP_COMMAND):].strip()

    if user_input == "Go to Python site":
        web_page_url = 'https://docs.python.org/3/'
        telebot_instance.send_message(message.chat.id, f'Open a web page: {web_page_url}')
        webbrowser.open('https://docs.python.org/3/')







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


        # Format the documentation
        formatted_doc = f"<b>{user_input.upper()} documentation:</b>\n\n{view_doc}"
        # log_message(message, DOCUMENTATION_COMMAND, message.text, formatted_doc)
        telebot_instance.send_message(message.chat.id, formatted_doc, parse_mode="HTML")


    except Exception as err:  # rewrite the error exception
        text = "Виникла помилка при пошуку\nабо перекладі документації."
        # log_message(message, DOCUMENTATION_COMMAND, user_input, text)
        telebot_instance.send_message(message.chat.id, text=text)
        print(f"Error: {str(err)}")

