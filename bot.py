"""import necessary libraries"""
import subprocess
import re
import telebot

from utils.KeyBoard.key_board import Keyboard
from utils.Handlers.help_button_handler import help_handler
from utils.Handlers.documentation_button_handler import documentation_handler
from utils.Handlers.callback_query_handler import callback_query_handler
from utils.Handlers.check_syntax_handler import check_syntax

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


@telebot_instance.message_handler(commands = ['check_code'])
def check_code(message):
    """
    :param message: create a temporary file and write the code into it
    :return: send message to user
    """
    try:
        code = message.text.split(maxsplit = 1)[1].strip()
    except IndexError:
        bot.send_message(message.chat.id, "Будь ласка, вкажіть код для перевірки.")
        return

    # Create a temporary file and write the code into it
    with open('tmp.py', 'w', encoding = 'utf-8') as checked_file:
        checked_file.write(code + "\n")

    # Check PEP8 style
    pep8_output = check_style('tmp.py')

    # Check syntax
    syntax_errors = check_syntax(message)


    result = ""

    if syntax_errors:
        result += f"У вашому коді є синтаксична помилка:\n{syntax_errors}\n"
    else:
        result += "Код не має синтаксичних помилок.\n"

    if pep8_output:
        cleaned_output = re.sub(r'\*.*?\*\* Module tmp\ntmp.py:\d+:\d+: ', '', pep8_output)
        result += f"\nУ вашому коді помилка PEP-8:\n{cleaned_output}"
    else:
        result += "\nКод не має помилок PEP-8."


    telebot_instance.send_message(message.chat.id, result)


def check_style(message):
    """Compare this snippet from data/bot_token.txt:"""
    result = subprocess.run(['pylint', message],
                            stdout = subprocess.PIPE,
                            stderr = subprocess.PIPE,
                            check = False)  # check=False to not raise an exception
    output = result.stdout.decode('utf-8') + result.stderr.decode('utf-8')
    return output if output else None


def check_syntax(message):
    """Compare this snippet from tmp.py:"""
    try:
        # create a subprocess to run python command with the file
        with subprocess.Popen(['python', 'tmp.py'], stdin = subprocess.PIPE,
                              stdout = subprocess.PIPE,
                              stderr = subprocess.PIPE,
                              shell = False) as process:
            # write the code to the subprocess stdin and close it
            error = process.communicate()

        # if there is an error, send it as a message to the user
        if error[1]:
            # remove the unnecessary from the error message
            error = error[1].decode().split('\n')[-2]

          
    except subprocess.CalledProcessError as check_syntax_error:
        # if there is an error while running the subprocess, send it as a message to the user
        telebot_instance.send_message(message.chat.id, f"Виникла помилка при перевірці синтаксису:"
                                                       f"\n{check_syntax_error}")




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




bot.callback_query_handler(func=lambda call: True)(callback_query_handler)

# start polling for new messages
if __name__ == '__main__':


    telebot_instance.polling(none_stop = True, timeout = 60)

