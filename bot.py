"""import necessary libraries"""
import subprocess
import os
import telebot

from utils.KeyBoard.key_board import create_keyboard

# set the file path for the token
FILE_NAME = 'data/bot_token.txt'

# read the token from the file
with open(FILE_NAME, 'r', encoding='utf-8') as file:
    TOKEN = file.read().strip()

# create a telebot instance using the token
bot = telebot.TeleBot(TOKEN)


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
    keyboard = create_keyboard()
    bot.send_message("Привіт! Я бот для взаємодії з користувачами. "
                     "Якщо вам потрібна допомога, використовуйте "
                     "клавіатуру нижче.",
                     str(message.chat.id),
                     reply_markup=keyboard)


@bot.message_handler(commands=['check_syntax'])
def check_syntax(message):
    """get the code to check from the message
    run the code in a subprocess and capture the output and errors"""

    # Check if there is code to check
    try:
        code = message.text.split(maxsplit=1)[1].strip()
    except IndexError:
        bot.send_message(message.chat.id, "Будь ласка, вкажіть код для перевірки.")
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
            bot.send_message(message.chat.id, f"У вашому коді є синтаксичка помилка:\n\n{error}")
        # if there is no error, send a message indicating that the syntax is ok
        else:
            bot.send_message(message.chat.id, "Синтаксис правильный.")

    except subprocess.CalledProcessError as check_syntax_error:
        # if there is an error while running the subprocess, send it as a message to the user
        bot.send_message(message.chat.id, f"Виникла помилка при перевірці синтаксису:"
                                          f"\n{check_syntax_error}")


# обробник для клавіш
@bot.message_handler(func=lambda message: True)
def echo_all(message):
    """
    This function takes a Telegram message as an argument
    and uses the message text to generate a reply.
    If the message text matches one of the predefined options,
    a corresponding reply is sent to the user.
    If not, a keyboard with options is displayed.

    Args:
    message (telegram.Message): A Telegram message object.

    Returns:
    None
    """
    if message.text == 'Пошук по документації':
        bot.reply_to(message, 'Ви натиснули кнопку Пошук по документації')
    elif message.text == 'Уроки':
        bot.reply_to(message, 'Ви натиснули кнопку Уроки')
    elif message.text == 'Запит на підказку':
        bot.reply_to(message, 'Ви натиснули кнопку Запит на підказку')
    elif message.text == 'Допомога по боту':
        bot.reply_to(message, 'Наш бот має такі команди: /help')
    else:
        keyboard = create_keyboard()
        bot.reply_to(message, 'Виберіть опцію з клавіатури нижче', reply_markup=keyboard)


# start polling for new messages
if __name__ == '__main__':
    bot.polling()
