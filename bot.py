"""Imports"""
import telebot

from utils.Handlers.callback_query_handler import callback_query_handler
from utils.Handlers.check_code_handler import check_code
from utils.Handlers.documentation_handler import search_documentation
from utils.Handlers.help_handler import help_handler
from utils.KeyBoard.key_board import Keyboard
from utils.Modes import MODE_DOCUMENTATION, MODE_MAIN_MENU, MODE_CHECK_CODE


class Bot:
    """
    This class implements the bot
    """

    def __init__(self, token_file):
        self.inline_keyboard = None
        self.bot = None
        self.token_file = token_file
        self.current_mode = MODE_MAIN_MENU


    def run(self):
        """
        This method runs the bot
        :return:
        """
        # read the token from the file
        with open(self.token_file, 'r', encoding='utf-8') as file:
            token = file.read().strip()

        # create a telebot instance using the token
        self.bot = telebot.TeleBot(token)

        # create an instance of InlineKeyboardMarkup
        self.inline_keyboard = Keyboard()

    def get_bot(self):
        """
        This method returns the bot
        """
        return self.bot

    def set_current_mode(self, mode):
        """
        This method sets the current mode
        :param mode:
        :return:
        """
        self.current_mode = mode


bot = Bot('data/bot_token.txt')
bot.run()

telebot_instance = bot.get_bot()


@telebot_instance.message_handler(commands=['start'])
def start_handler(message):
    """
    This method sends the welcome message
    :param message:
    :return:
    """
    telebot_instance.send_message(message.chat.id, "Welcome to my bot!",
                                  reply_markup=bot.inline_keyboard.get_keyboard())


@telebot_instance.callback_query_handler(func=lambda call: True)
def handle_callback_query(call):
    """This handler allows to use callback query with pressing designated inline keyboard buttons"""
    if call.data.find(MODE_DOCUMENTATION) != -1:
        bot.current_mode = MODE_DOCUMENTATION
    elif call.data.find(MODE_CHECK_CODE) != -1:
        bot.current_mode = MODE_CHECK_CODE
    elif call.data.find(MODE_MAIN_MENU) != -1:
        bot.current_mode = MODE_MAIN_MENU
    callback_query_handler(call, telebot_instance, bot.inline_keyboard)


# Додано новий обробник повідомлень для відображення поточного режиму
@telebot_instance.message_handler(func=lambda message: True)
def display_current_mode(message):
    """
    This method displays the current mode
    :param message:
    :return:
    """
    if bot.current_mode == MODE_MAIN_MENU:
        telebot_instance.send_message(message.chat.id, "Знаходитесь в головному меню.")
    elif bot.current_mode == MODE_DOCUMENTATION:
        telebot_instance.send_message(message.chat.id, "Знаходитесь в режимі документації.")
        search_documentation(message, telebot_instance)
    elif bot.current_mode == MODE_CHECK_CODE:
        telebot_instance.send_message(message.chat.id, "Знаходитесь в режимі перевірки коду.")
        check_code(message, telebot_instance)


telebot_instance.callback_query_handler(func=lambda call: True)(callback_query_handler)

# start polling for new messages
if __name__ == '__main__':
    telebot_instance.polling(none_stop=True, timeout=60)
