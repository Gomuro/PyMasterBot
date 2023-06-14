"""search_documentation handler function"""
import pydoc

from utils.bot_logger import log_message

DOCUMENTATION_COMMAND = "/documentation"

def search_documentation(message, telebot_instance):
    """
    This function searches the documentation
    :param telebot_instance:
    :param message:
    :return:
    """
    user_input = message.text.strip()
    if user_input.find("documentation") != -1:
        user_input = message.text.strip()
        user_input = user_input[len(DOCUMENTATION_COMMAND):].strip()

    if not user_input:
        text = "Будь ласка, введіть ключове слово для пошуку документації."
        # log_message(message, DOCUMENTATION_COMMAND, user_input, text)
        telebot_instance.send_message(message.chat.id, text = text)
        return  # Вирівняти з блоком if

    try:
        # Use pydoc to get the documentation
        doc = pydoc.render_doc(user_input)

        if not doc:
            text = "На жаль, не знайдено документації для даного запиту."
            # log_message(message, DOCUMENTATION_COMMAND, user_input, text)
            telebot_instance.send_message(message.chat.id,
                                          text = text
                                          )
            return

        # Remove the content after (...)
        index = doc.find("(...)")
        if index != -1:
            doc = doc[index + len("(...)"):]

        # Format the documentation
        formatted_doc = f"<b>{user_input} Documentation:</b>\n\n{doc}"
        # log_message(message, DOCUMENTATION_COMMAND, message.text, formatted_doc)
        telebot_instance.send_message(message.chat.id, formatted_doc, parse_mode = "HTML")
    except Exception as err:  # rewrite the error exception
        text = "Виникла помилка при пошуку\n" \
               "або перекладі документації."
        # log_message(message, DOCUMENTATION_COMMAND, user_input, text)
        telebot_instance.send_message(message.chat.id,
                                      text = text)
        print(f"Error: {str(err)}")
