""" This module allows to send designated message when the button been pressed"""
def documentation_handler(message, bot, inline_keyboard):
    """ This method allows to send designated message when the button been pressed"""
    bot.send_message(message.chat.id,
                     text="Якщо у вас є запитання щодо використання бота, "
                          "скористайтеся командою /help",
                     reply_markup=inline_keyboard.get_keyboard())
