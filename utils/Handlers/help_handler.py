"""import"""
from utils.bot_logger import log_message


def help_handler(message, telebot_instance, inline_keyboard):
    """ This method allows to send designated message when the button been pressed"""
    text = "Test version."
    log_message('/help', "", text)
    telebot_instance.send_message(message.chat.id,
                                  text = text,
                                  reply_markup = inline_keyboard.get_keyboard()
                                  )
