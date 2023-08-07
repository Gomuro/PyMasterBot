"""import"""
from Handlers.exception_handler import handle_exception
from utils.bot_logger import log_message

HELP_COMMAND = "/help"


def help_handler(message, telebot_instance, inline_keyboard):
    """ This method allows to send designated message when the button been pressed"""
    try:

        text = "I can help you with these commands:\n"\
               "/help - getting help on your question\n"\
               "/check_code - syntax checking\n"\
               "/documentation obtaining documentation"
        log_message(message, HELP_COMMAND, '', text)
        telebot_instance.send_message(message.chat.id,
                                      text=text,
                                      reply_markup=inline_keyboard.get_keyboard()
                                      )

    except Exception as e:
        handle_exception(e, telebot_instance)
