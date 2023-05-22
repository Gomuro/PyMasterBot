""" This module allows to send designated message when the button been pressed"""
def help_handler(message, bot, inline_keyboard):
    """ This method allows to send designated message when the button been pressed"""
    bot.send_message(message.chat.id,
                     text="Test version.",
                     reply_markup=inline_keyboard.get_keyboard()
                     )
