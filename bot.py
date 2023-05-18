"""import necessary libraries"""
import telebot

from utils.KeyBoard.key_board import Keyboard
from utils.Handlers.help_button_handler import help_handler
from utils.Handlers.documentation_button_handler import documentation_handler
from utils.Handlers.callback_query_handler import callback_query_handler
from utils.Handlers.check_syntax_handler import check_syntax

# set the file path for the token
FILE_NAME = 'data/bot_token.txt'

# read the token from the file
with open(FILE_NAME, 'r', encoding='utf-8') as file:
    TOKEN = file.read().strip()

# create a telebot instance using the token
bot = telebot.TeleBot(TOKEN)
inline_keyboard = Keyboard()


@bot.message_handler(commands=['start'])
def start_handler(message):
    """ This decoration method allows to send welcome message """
    bot.send_message(message.chat.id, "Welcome to my bot!",
                     reply_markup=inline_keyboard.get_keyboard())


@bot.message_handler(commands=['check_syntax'])
def check_syntax_handler(message):
    """This handler allows to send designated message when the button been pressed"""
    check_syntax(bot, message)


@bot.message_handler(commands=['help'])
def handle_help(message):
    """This handler allows to send designated message when the button been pressed"""
    help_handler(message, bot, inline_keyboard)


@bot.message_handler(commands=['documentation'])
def handle_documentation(message):
    """This handler allows to send designated message when the button been pressed"""
    documentation_handler(message, bot, inline_keyboard)


@bot.callback_query_handler(func=lambda call: True)
def handle_callback_query(call):
    """This handler allows to use callback query with pressing designated inline keyboard buttons"""
    callback_query_handler(call, bot, inline_keyboard)


bot.callback_query_handler(func=lambda call: True)(callback_query_handler)

# start polling for new messages
if __name__ == '__main__':
    bot.polling()
