import os
import telebot
from dotenv import load_dotenv
from Handlers.add_admin_handler import add_admin_function
from Handlers.add_lesson_handler import add_lesson_function
from Handlers.callback_query_handler import callback_query_handler
from Handlers.check_code_handler import check_code
from Handlers.documentation_handler import search_documentation
from utils.key_board import InlineKeyboard, ReplyKeyboard
from utils.modes import MODE_MAIN_MENU, MODE_DOCUMENTATION, MODE_CHECK_CODE, MODE_LESSON, MODE_HELP

from Handlers.add_test_task_handler import add_test_task_function
from Handlers.change_test_task_handler import change_test_task_function
from Handlers.request_help_handler import help_request_handler
from Handlers.csv_handler import handle_csv_lessons
from Handlers.csv_handler import handle_csv_test_tasks
from Handlers.add_level_handler import add_level_function




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
        self.reply_keyboard = None

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
        # create an instance of ReplyKeyboardMarkup
        self.reply_keyboard = ReplyKeyboard()

        # Add "HELP" button to the inline keyboard
        self.inline_keyboard.add_button("HELP", callback_data="/help")

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

    def add_test_task_handler(self, message):
        """
        This method adds a test_task
        """
        if message.text.find("/add_test_task") != -1:
            add_test_task_function(self.bot, message)

    def change_test_task_handler(self, message):
        """
        This method changes a test_task
        """
        if message.text.find("/change_test_task") != -1:
            change_test_task_function(self.bot, message)

    def add_level_handler(self, message):
        """
        This method adds a lesson
        """
        if message.text.find("/add_level") != -1:
            add_level_function(self.bot, message)

    def csv_tables_names_lessons(self, message):
        if message.document.file_name == 'lessons.csv':
            handle_csv_lessons(self.bot, message, message.document)
        elif message.document.file_name == 'test_tasks.csv':
            handle_csv_test_tasks(self.bot, message, message.document)
        elif message.document.file_name != 'lessons.csv' or 'test_tasks.csv':
            self.bot.send_message(message.chat.id,
                                          "Будь ласка, відправте файл у форматі CSV з такою самою назвою"
                                          " як нава таблиці в Базі Даннх.")

    def handle_callback_query(self, call):
        """This handler allows using callback query with pressing designated inline keyboard buttons
        if call.data.find(MODE_DOCUMENTATION) != -1:
            self.current_mode = MODE_DOCUMENTATION
        elif call.data.find(MODE_CHECK_CODE) != -1:
            self.current_mode = MODE_CHECK_CODE
        elif call.data.find(MODE_MAIN_MENU) != -1:
            self.current_mode = MODE_MAIN_MENU

        callback_query_handler(call, self.bot, self.inline_keyboard) """

        if call.data.find(MODE_CHECK_CODE) != -1:
            self.current_mode = MODE_CHECK_CODE
        elif call.data.find(MODE_HELP) != -1:
            self.current_mode = MODE_HELP
        elif call.data.find(MODE_MAIN_MENU) != -1:
            self.current_mode = MODE_MAIN_MENU
        else:
            self.current_mode = MODE_DOCUMENTATION
        callback_query_handler(call, self.bot, self.inline_keyboard, self.reply_keyboard)

    def display_current_mode(self, message):
        """
        This method displays the current mode

        # self.bot.delete_message(message.chat.id, message.message_id)
        if self.current_mode == MODE_MAIN_MENU:
            self.bot.send_message(message.chat.id, "You are in the main menu mode.",
                                  reply_markup=self.inline_keyboard.get_keyboard())
        elif self.current_mode == MODE_DOCUMENTATION:
            self.bot.delete_message(message.chat.id, message.message_id)
            self.bot.send_message(message.chat.id, "You are in documentation mode.",
                                  reply_markup=self.inline_keyboard.get_keyboard())
            search_documentation(message, self.bot)
        elif self.current_mode == MODE_CHECK_CODE:
            self.bot.send_message(message.chat.id, "You are in check code mode.",
                                  reply_markup=self.inline_keyboard.get_keyboard())
            check_code(message, self.bot)
        elif self.current_mode == MODE_LESSON:
            self.bot.send_message(message.chat.id, "You are in lesson mode.",
                                  reply_markup=self.inline_keyboard.get_keyboard())  """

        if self.current_mode == MODE_MAIN_MENU:
            self.bot.send_message(message.chat.id, "You are in the main menu mode.",
                                  reply_markup=self.inline_keyboard.get_keyboard())
        elif self.current_mode == MODE_DOCUMENTATION:
            self.bot.delete_message(message.chat.id, message.message_id)
            self.bot.send_message(message.chat.id, "You are in documentation mode.",
                                  reply_markup=self.inline_keyboard.get_keyboard())
            search_documentation(message, self.bot)
        elif self.current_mode == MODE_CHECK_CODE:
            self.bot.send_message(message.chat.id, "You are in check code mode.",
                                  reply_markup=self.inline_keyboard.get_keyboard())
            check_code(message, self.bot)
        elif self.current_mode == MODE_LESSON:
            self.bot.send_message(message.chat.id, "You are in lesson mode.",
                                  reply_markup=self.inline_keyboard.get_keyboard())
        elif self.current_mode == MODE_HELP:
            self.bot.send_message(message.chat.id, "You are in the help mode.",
                                  reply_markup=self.inline_keyboard.get_keyboard())
            help_request_handler(message, self.bot)
        # Handle the "HELP" button separately
        if message.text == "HELP":
            self.bot.send_message(message.chat.id, "This is the help message.")
