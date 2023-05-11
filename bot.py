"""import necessary libraries"""
import subprocess
import time
import re
import telebot

from utils.KeyBoard.key_board import Keyboard

# set the file path for the token
FILE_NAME = 'data/bot_token.txt'

# read the token from the file
with open(FILE_NAME, 'r', encoding = 'utf-8') as file:
    TOKEN = file.read().strip()

# create a telebot instance using the token
bot = telebot.TeleBot(TOKEN)
inline_keyboard = Keyboard()


# handle the /start command
@bot.message_handler(commands = ['start'])
def start(message):
    """
    Send a welcome message to the user with a keyboard for further interaction.
    Args: message (telebot.types.Message): The message object that triggered the function.
    Returns: None
    """
    bot.send_message(message.chat.id,
                     "Привіт! Я бот який може перевірити ваш код.\n"
                     "Напишіть одним повідомленням /check_code - ваш код.",
                     reply_markup = inline_keyboard.get_keyboard())


@bot.message_handler(commands = ['check_code'])
def check_code(message):
    """
    :param message: create a temporary file and write the code into it
    :return: send message to user
    """
    time.sleep(1)
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
        cleaned_output = re.sub(r'tmp\.py:\d+:\d+: ', '', pep8_output)
        result += f"У вашому коді помилка PEP-8:\n{cleaned_output}"
    else:
        result += "Код не має помилок PEP-8."

    bot.send_message(message.chat.id, result)


def check_style(message):
    """Compare this snippet from data/bot_token.txt:"""
    result = subprocess.run(['pycodestyle', message],
                            stdout = subprocess.PIPE,
                            stderr = subprocess.PIPE,
                            check = False)  # check=False to not raise an exception
    output = result.stdout.decode('utf-8') + result.stderr.decode('utf-8')
    return output if output else None


def check_syntax(message):
    """Check syntax of the code and return the output"""
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
            return error
        return None

    except subprocess.CalledProcessError as check_syntax_error:
        # if there is an error while running the subprocess, send it as a message to the user
        bot.send_message(message.chat.id, f"Виникла помилка при перевірці синтаксису:"
                                          f"\n{check_syntax_error}")
        return check_syntax_error


@bot.message_handler(commands = ['help'])
def help_handler(message):
    """ This method allows to send designated message when the button been pressed"""
    bot.send_message(message.chat.id,
                     text = "Я можу допомогти вам з цими командами:\n"
                            "/help - допомога\n"
                            "/check_syntax - перевірка синтаксису\n"
                            "/documentation - документація",
                     reply_markup = inline_keyboard.get_keyboard()
                     )


@bot.message_handler(commands = ['documentation'])
def documentation_handler(message):
    """ This method allows to send designated message when the button been pressed"""
    bot.send_message(message.chat.id,
                     text = "Якщо у вас є запитання щодо використання бота, "
                            "скористайтеся командою /help",
                     reply_markup = inline_keyboard.get_keyboard())


@bot.callback_query_handler(func = lambda call: True)
def callback_query_handler(call):
    """ This method allows to send designated message when the button been pressed"""
    if call.data == '/help':
        bot.answer_callback_query(callback_query_id = call.id)
        bot.send_message(chat_id = call.message.chat.id,
                         text = "Я можу допомогти вам з цими командами:\n"
                                "/help - допомога\n"
                                "/check_syntax - перевірка синтаксису\n"
                                "/documentation - документація",
                         reply_markup = inline_keyboard.get_keyboard()
                         )


    elif call.data == '/check_syntax':
        bot.answer_callback_query(callback_query_id = call.id)
        bot.send_message(chat_id = call.message.chat.id,
                         text = "Відправте код, який потрібно перевірити.",
                         reply_markup = inline_keyboard.get_keyboard())
    elif call.data == '/documentation':
        bot.answer_callback_query(callback_query_id = call.id)
        bot.send_message(chat_id = call.message.chat.id,
                         text = ("Якщо у вас є запитання щодо використання бота, "
                                 "скористайтеся командою /help"),
                         reply_markup = inline_keyboard.get_keyboard())

    else:
        bot.answer_callback_query(callback_query_id = call.id, text = "Такої команди не існує!")


# start polling for new messages
if __name__ == '__main__':
    bot.polling()
