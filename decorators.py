import os
import telebot
from dotenv import load_dotenv

from Handlers.add_test_task_by_level_handler import add_easy_test_task_function, add_middle_test_task_function, \
    add_hard_test_task_function
from Handlers.add_code_task_by_level_handler import add_easy_code_task_function, add_middle_code_task_function, \
    add_hard_code_task_function
from Handlers.add_view_comments import process_comments
from change_modes import BotProcessor

from Handlers.add_admin_handler import add_admin_function
from Handlers.add_lesson_handler import add_lesson_function
from Handlers.callback_query_handler import callback_query_handler
from Handlers.check_code_handler import check_code
from Handlers.documentation_handler import search_documentation
from Handlers.add_code_task_handler import add_code_task_function
from Handlers.change_code_task_handler import change_code_task_function
from Handlers.choose_code_task_handler import process_code_task_level
from Handlers.add_test_task_handler import add_test_task_function
from Handlers.change_test_task_handler import change_test_task_function
from Handlers.choose_test_task_handler import process_test_task_level
from Handlers.choose_lesson_handler import process_lesson_topic
from Handlers.request_help_handler import help_request_handler
from Handlers.csv_handler import handle_csv_lessons
from Handlers.csv_handler import handle_csv_test_tasks
from Handlers.csv_handler import handle_csv_code_tasks
from Handlers.add_level_handler import add_level_function
from Handlers.premium_status_handler import premium_status_function
from Handlers.account_handler import account_function


from utils.key_board import InlineKeyboard, ReplyKeyboard
from utils.modes import MODE_MAIN_MENU


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

        self.bot_processor = BotProcessor()

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

    def get_bot(self):
        """
        This method returns the bot
        """
        return self.bot

    def delete_message(self, chat_id, message_id):
        self.bot.delete_message(chat_id, message_id)

    def start_handler(self, message):
        """
        This method sends the welcome message
        """
        from bot import bot_db
        # print(self.bot_processor.get_current_mode())
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
            print(self.bot_processor.get_current_mode())
            add_lesson_function(self.bot, message)

    def add_admin_handler(self, message):
        """
        This method adds an admin
        """
        if message.text.find("/add_admin") != -1:
            print(self.bot_processor.get_current_mode())
            add_admin_function(self.bot, message)

    def add_test_task_handler(self, message):
        """
        This method adds a test_task
        """
        if message.text.find("/add_test_task") != -1:
            add_test_task_function(self.bot, message)

    def add_test_task_by_level_handler(self, message):
        """
        This method adds a test_task based on the level.
        """

        if message.text.find("/add_easy_test_task") != -1:
            add_easy_test_task_function(self.bot, message)
        elif message.text.find("/add_middle_test_task") != -1:
            add_middle_test_task_function(self.bot, message)
        elif message.text.find("/add_hard_test_task") != -1:
            add_hard_test_task_function(self.bot, message)

    def change_test_task_handler(self, message):
        """
        This method changes a test_task
        """
        if message.text.find("/change_test_task") != -1:
            change_test_task_function(self.bot, message)

    def add_code_task_handler(self, message):
        """
        This method adds a code_task
        """
        if message.text.find("/add_test_task") != -1:
            add_code_task_function(self.bot, message)

    def add_code_task_by_level_handler(self, message):
        """
        This method adds a code_task based on the level.
        """

        if message.text.find("/add_easy_code_task") != -1:
            add_easy_code_task_function(self.bot, message)
        elif message.text.find("/add_middle_code_task") != -1:
            add_middle_code_task_function(self.bot, message)
        elif message.text.find("/add_hard_code_task") != -1:
            add_hard_code_task_function(self.bot, message)

    def change_code_task_handler(self, message):
        """
        This method changes a test_task
        """
        if message.text.find("/change_code_task") != -1:
            change_code_task_function(self.bot, message)

    def add_level_handler(self, message):
        """
        This method adds a lesson
        """
        if message.text.find("/add_level") != -1:
            add_level_function(self.bot, message)

    def send_error_message(self, error_message):
        self.bot.send_message(os.getenv('OWNER_CHAT_ID'), f"Error in bot:\n\n{error_message}")

    def csv_tables_names_lessons(self, message):
        if message.document.file_name == 'lessons.csv':
            handle_csv_lessons(self.bot, message, message.document)
        elif message.document.file_name == 'test_tasks.csv':
            handle_csv_test_tasks(self.bot, message, message.document)
        elif message.document.file_name == 'code_tasks.csv':
            handle_csv_code_tasks(self.bot, message, message.document)
        elif message.document.file_name != 'lessons.csv' or 'test_tasks.csv':
            self.bot.send_message(message.chat.id, "Please send the file in CSV format with the same name,\n"
                                                   "as a table name in the DATABASE.")

    def handle_callback_query(self, call):

        """This handler allows using callback query with pressing designated inline keyboard buttons"""
        self.bot_processor.message_handler(call)  # Set the current mode
        callback_query_handler(call, self.bot, self.inline_keyboard, self.reply_keyboard)

    def display_current_mode(self, message):
        """
        This method displays the current mode
        """
        if self.bot_processor.is_mode_main_menu():
            self.bot.send_message(message.chat.id, "You are in the main menu mode.",
                                  reply_markup=self.inline_keyboard.get_keyboard())
        elif self.bot_processor.is_mode_documentation():
            self.bot.delete_message(message.chat.id, message.message_id)
            self.bot.send_message(message.chat.id, "You are in documentation mode.",
                                  reply_markup=self.inline_keyboard.get_keyboard())
            search_documentation(message, self.bot)
        elif self.bot_processor.is_mode_check_code():
            self.bot.send_message(message.chat.id, "You are in check code mode.",
                                  reply_markup=self.inline_keyboard.get_keyboard())
            check_code(message, self.bot)
        elif self.bot_processor.is_mode_lesson():
            self.bot.send_message(message.chat.id, "You are in lesson mode.",
                                  reply_markup=self.inline_keyboard.get_keyboard())
            process_lesson_topic(message, self.bot)
        elif self.bot_processor.is_mode_testing():
            self.bot.send_message(message.chat.id, "You are in testing mode.",
                                  reply_markup=self.inline_keyboard.get_keyboard())
            process_test_task_level(message, self.bot)
        elif self.bot_processor.is_mode_coding():
            self.bot.send_message(message.chat.id, "You are in coding mode.",
                                  reply_markup=self.inline_keyboard.get_keyboard())
            process_code_task_level(message, self.bot)
        elif self.bot_processor.is_mode_account():
            self.bot.delete_message(message.chat.id, message.message_id)
            self.bot.send_message(message.chat.id, "You are in account mode.",
                                  reply_markup=self.inline_keyboard.get_keyboard())
            account_function(message, self.bot)
        elif self.bot_processor.is_mode_comments():
            self.bot.send_message(message.chat.id, "You are in comments mode.",
                                  reply_markup=self.inline_keyboard.get_keyboard())
            process_comments(self.bot, message)
        elif self.bot_processor.is_mode_help():
            self.bot.send_message(message.chat.id, "You are in help mode.",
                                  reply_markup=self.inline_keyboard.get_keyboard())
            help_request_handler(message, self.bot)
        elif self.bot_processor.is_mode_premium():
            self.bot.send_message(message.chat.id, "You are in 'Premium' mode.",
                                  reply_markup=self.inline_keyboard.get_keyboard())
            premium_status_function(message, self.bot)
            
        # Handle the "HELP" button separately
        if message.text == "HELP":
            self.bot.send_message(message.chat.id, "This is the help message.",
                                  reply_markup=self.inline_keyboard.get_keyboard())           
            
           