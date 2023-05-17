"""Imports"""
import subprocess
import os
import telebot

from utils.KeyBoard.key_board import Keyboard
from utils.documentation_finder import search_documentation


class Bot:
    """
    This class implements the bot
    """

    def __init__(self, token_file):
        self.inline_keyboard = None
        self.bot = None
        self.token_file = token_file
        self.current_mode = "main_menu"  # Початковий режим

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


bot = Bot('data/bot_token.txt')
bot.run()

telebot_instance = bot.get_bot()

MODE_DOCUMENTATION = "documentation"
MODE_MAIN_MENU = "main_menu"


@telebot_instance.message_handler(commands=['start'])
def start_handler(message):
    """
    This method sends the welcome message
    :param message:
    :return:
    """
    telebot_instance.send_message(message.chat.id, "Welcome to my bot!",
                                  reply_markup=bot.inline_keyboard.get_keyboard())


@telebot_instance.message_handler(commands=['check_syntax'])
def check_syntax(message):
    """get the code to check from the message
    run the code in a subprocess and capture the output and errors"""

    # Check if there is code to check
    try:
        code = message.text.split(maxsplit=1)[1].strip()
    except IndexError:
        telebot_instance.send_message(message.chat.id, "Будь ласка, вкажіть код для перевірки.")
        return

    # Remove the existing temporary file if it exists
    if os.path.exists('tmp.py'):
        os.remove('tmp.py')

    # Create a temporary file and write the code into it
    with open('tmp.py', 'w', encoding='utf-8') as checked_file:
        checked_file.write(code)

    try:
        # create a subprocess to run python command with the file
        with subprocess.Popen(['python', 'tmp.py'], stdin=subprocess.PIPE,
                              stdout=subprocess.PIPE,
                              stderr=subprocess.PIPE,
                              shell=False) as process:
            # write the code to the subprocess stdin and close it
            error = process.communicate()

        # if there is an error, send it as a message to the user
        if error[1]:
            # remove the unnecessary from the error message
            error = error[1].decode().split('\n')[-2]
            telebot_instance.send_message(message.chat.id,
                                          f"У вашому коді є синтаксичка помилка:\n\n{error}"
                                          )
        # if there is no error, send a message indicating that the syntax is ok
        else:
            telebot_instance.send_message(message.chat.id, "Синтаксис правильный.")

    except subprocess.CalledProcessError as check_syntax_error:
        # if there is an error while running the subprocess, send it as a message to the user
        telebot_instance.send_message(message.chat.id, f"Виникла помилка при перевірці синтаксису:"
                                                       f"\n{check_syntax_error}")


@telebot_instance.message_handler(commands=['help'])
def help_handler(message):
    """
    This method sends the help message
    :param message:
    :return:
    """
    telebot_instance.send_message(message.chat.id,
                                  text="Я можу допомогти вам з цими командами:\n"
                                       "/help - допомога\n"
                                       "/check_syntax - перевірка синтаксису\n"
                                       "/documentation - документація",
                                  reply_markup=bot.inline_keyboard.get_keyboard()
                                  )


@telebot_instance.message_handler(commands=['documentation'])
def documentation_handler(message):
    """
    use the search_documentation function
    :param message:
    :return:
    """
    bot.current_mode = MODE_DOCUMENTATION
    search_documentation(message, telebot_instance)


@telebot_instance.callback_query_handler(func=lambda call: True)
def callback_query_handler(call):
    """
    This method handles the callback query
    :param call:
    :return:
    """
    if call.data == '/help':
        telebot_instance.answer_callback_query(callback_query_id=call.id)
        telebot_instance.send_message(chat_id=call.message.chat.id,
                                      text="Я можу допомогти вам з цими командами:\n"
                                           "/help - допомога\n"
                                           "/check_syntax - перевірка синтаксису\n"
                                           "/documentation - документація",
                                      reply_markup=bot.inline_keyboard.get_keyboard()
                                      )
    elif call.data == '/check_syntax':
        telebot_instance.answer_callback_query(callback_query_id=call.id)
        telebot_instance.send_message(chat_id=call.message.chat.id,
                                      text="Відправте код, який потрібно перевірити.",
                                      reply_markup=bot.inline_keyboard.get_keyboard()
                                      )
    elif call.data == '/documentation':
        telebot_instance.answer_callback_query(callback_query_id=call.id)
        telebot_instance.send_message(chat_id=call.message.chat.id,
                                      text="Введіть назву модуля, функції або класу, "
                                           "\nдля якого потрібно знайти документацію.",
                                      reply_markup=bot.inline_keyboard.get_keyboard()
                                      )
        bot.current_mode = MODE_DOCUMENTATION


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


# start polling for new messages
if __name__ == '__main__':
    telebot_instance.polling()
