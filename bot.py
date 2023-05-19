"""import necessary libraries"""
import subprocess
import re
import logging
import os
import json
import datetime
import telebot

from utils.KeyBoard.key_board import Keyboard

# set the file path for the token
FILE_NAME = 'data/bot_token.txt'

# read the token from the file
with open(FILE_NAME, 'r', encoding = 'utf-8') as token_file:
    TOKEN = token_file.read().strip()

# create a telebot instance using the token
bot = telebot.TeleBot(TOKEN)
inline_keyboard = Keyboard()

TMP_FILE = 'tmp.py'
RELATIVE_PATH = 'data/logs'
ABSOLUTE_PATH = os.path.abspath(RELATIVE_PATH)
LOG_FILE_FORMAT = '%Y-%m-%d.json'


def setup_logging():
    """Logger setup"""
    os.makedirs(ABSOLUTE_PATH, exist_ok = True)

    logger = logging.getLogger('PyMasterBot')
    logger.setLevel(logging.INFO)

    current_date = datetime.datetime.now().strftime(LOG_FILE_FORMAT)
    log_file = os.path.join(ABSOLUTE_PATH, current_date)
    file_handler = logging.FileHandler(log_file)

    logger.addHandler(file_handler)

    return logger


def log_message(command, code, text):
    """
    Logs the message details to a JSON log file.

    Args:
        command (str): The command that triggered the logging.
        code (str): The code associated with the log message.
        text (str): The text message to be logged.

    Returns:
        None
    """
    timestamp = datetime.datetime.now()

    log_data = {
        'timestamp': timestamp.strftime('%Y-%m-%d %H:%M:%S'),
        'command': command,
        'code': code,
        'response': text,
    }

    log_file = os.path.join(ABSOLUTE_PATH, datetime.datetime.now().strftime(LOG_FILE_FORMAT))

    if not os.path.exists(log_file):
        with open(log_file, 'w', encoding = 'utf-8') as file:
            json.dump(log_data, file)
    else:
        with open(log_file, 'r', encoding = 'utf-8') as file:
            try:
                existing_data = json.load(file)
            except json.JSONDecodeError:
                existing_data = {'data': []}

        existing_data['data'].append(log_data)

        with open(log_file, 'w', encoding = 'utf-8') as file:
            json.dump(existing_data, file, ensure_ascii = False, indent = 4)


# handle the /start command
@bot.message_handler(commands=['start'])
def start(message):
    """
    Send a welcome message to the user with a keyboard for further interaction.
    Args:
        message (telebot.types.Message): The message object that triggered the function.
    Returns:
        None
    """
    text = 'Привіт! Я бот, який може перевірити ваш код.\n' \
           'Напишіть одним повідомленням /check_code - ваш код.'
    log_message('/start', "", text,)
    bot.send_message(message.chat.id,
                     text=text,
                     reply_markup=inline_keyboard.get_keyboard())


@bot.message_handler(commands = ['check_code'])
def check_code(message):
    """
    :param message: create a temporary file and write the code into it
    :return: send message to user
    """
    try:
        code = message.text.split(maxsplit = 1)[1].strip()
    except IndexError:
        text = 'Будь ласка, вкажіть код для перевірки.'
        bot.send_message(message.chat.id, text = text)
        return

    # Create a temporary file and write the code into it
    with open(TMP_FILE, 'w', encoding = 'utf-8') as checked_file:
        checked_file.write(code + "\n")

    # Check PEP8 style
    pep8_output = check_style()

    # Check syntax
    syntax_errors = check_syntax()

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

    log_message('/check_code', code, result)

    bot.send_message(message.chat.id, result)


def check_style():
    """Compare this snippet from data/bot_token.txt:"""
    result = subprocess.run(['pylint', TMP_FILE],
                            stdout = subprocess.PIPE,
                            stderr = subprocess.PIPE,
                            check = False)  # check=False to not raise an exception
    output = result.stdout.decode('utf-8') + result.stderr.decode('utf-8')
    cleaned_output = output.replace(
        '------------------------------------------------------------------', '')

    return cleaned_output.strip() if cleaned_output else None


def check_syntax():
    """Compare this snippet from tmp.py:"""
    # create a subprocess to run python command with the file
    with subprocess.Popen(['python', TMP_FILE], stdin = subprocess.PIPE,
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


# start polling for new messages
if __name__ == '__main__':
    bot.polling()
