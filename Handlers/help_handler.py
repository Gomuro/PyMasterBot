"""import"""
import os

from utils.bot_logger import log_message

HELP_COMMAND = "/help"


def help_handler(message, telebot_instance, inline_keyboard):
    """ This method allows to send designated message when the button been pressed"""
    try:

        text = "Я можу допомогти вам з цими командами:\n"\
               "/help - допомога\n"\
               "/check_code - перевірка синтаксису\n"\
               "/documentation - документація"
        log_message(message, HELP_COMMAND, '', text)
        telebot_instance.send_message(message.chat.id,
                                      text=text,
                                      reply_markup=inline_keyboard.get_keyboard()
                                      )

    except Exception as e:
        error_message = str(e)
        telebot_instance.send_message(os.getenv('OWNER_CHAT_ID'), f"Помилка в боті:\n{error_message}")
