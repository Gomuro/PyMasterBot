import os
import telebot
from dotenv import load_dotenv
from utils.Handlers.add_admin_handler import add_admin_function
from utils.Handlers.add_lesson_handler import add_lesson_function
from utils.Handlers.callback_query_handler import callback_query_handler
from utils.Handlers.check_code_handler import check_code
from utils.Handlers.documentation_handler import search_documentation
from utils.KeyBoard.key_board import InlineKeyboard
from utils.modes import MODE_MAIN_MENU, MODE_DOCUMENTATION, MODE_CHECK_CODE, MODE_LESSON


class Bot:
    """
    This class implements the bot
    """

    def __init__(self, token):
        self.inline_keyboard = None
        self.bot = None
        self.chat_id = None
        self.token = token
        self.current_mode = MODE_MAIN_MENU

    def run(self):
        """
        This method runs the bot
        """
        load_dotenv()
        token = os.getenv('TOKEN')
        # create a telebot instance using the token
        self.bot = telebot.TeleBot(token)
        # create an instance of InlineKeyboardMarkup
        self.inline_keyboard = InlineKeyboard()

    def get_bot(self):
        """
        This method returns the bot
        """
        return self.bot

    def set_current_mode(self, mode):
        """
        This method sets the current mode
        """
        self.current_mode = mode

    def delete_message(self, chat_id, message_id):
        self.bot.delete_message(chat_id, message_id)

    def start_handler(self, message):
        """
        This method sends the welcome message
        """
        from bot import bot_db
        if not bot_db.check_user_exists(message.chat.id):
            bot_db.add_user(message.chat.id, message.chat.first_name, message.chat.username)
            self.bot.send_message(message.chat.id, f"Welcome to my bot, {message.chat.first_name}!",
                                  reply_markup=self.inline_keyboard.get_keyboard())
        else:
            self.bot.send_message(message.chat.id, f"Welcome back, {message.chat.first_name}!",
                                  reply_markup=self.inline_keyboard.get_keyboard())

    def add_lesson_handler(self, message):
        """
        This method adds a lesson
        """
        if message.text.find("/add_lesson") != -1:
            add_lesson_function(self.bot, message)

    def add_admin_handler(self, message):
        """
        This method adds an admin
        """
        if message.text.find("/add_admin") != -1:
            add_admin_function(self.bot, message)

    def handle_callback_query(self, call):
        """This handler allows using callback query with pressing designated inline keyboard buttons"""
        if call.data.find(MODE_DOCUMENTATION) != -1:
            self.current_mode = MODE_DOCUMENTATION
        elif call.data.find(MODE_CHECK_CODE) != -1:
            self.current_mode = MODE_CHECK_CODE
        elif call.data.find(MODE_MAIN_MENU) != -1:
            self.current_mode = MODE_MAIN_MENU
        callback_query_handler(call, self.bot, self.inline_keyboard)

    def display_current_mode(self, message):
        """
        This method displays the current mode
        """
        if self.current_mode == MODE_MAIN_MENU:
            self.bot.send_message(message.chat.id, "Вы находитесь в главном меню.")
        elif self.current_mode == MODE_DOCUMENTATION:
            self.bot.send_message(message.chat.id, "Вы находитесь в режиме документации.")
            search_documentation(message, self.bot)
        elif self.current_mode == MODE_CHECK_CODE:
            self.bot.send_message(message.chat.id, "Вы находитесь в режиме проверки кода.")
            check_code(message, self.bot)
        elif self.current_mode == MODE_LESSON:
            self.bot.send_message(message.chat.id, "Вы находитесь в режиме занятия.")
