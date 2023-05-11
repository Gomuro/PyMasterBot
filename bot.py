"""import necessary libraries"""
import os
import subprocess
import telebot
from utils.KeyBoard.key_board import Keyboard

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


@bot.message_handler(commands=['help'])
def help_handler(message):
    """ This method allows to send designated message when the button been pressed"""
    bot.send_message(message.chat.id,
                     text="Я можу допомогти вам з цими командами:\n"
                          "/help - допомога\n"
                          "/check_syntax - перевірка синтаксису\n"
                          "/documentation - документація",
                     reply_markup=inline_keyboard.get_keyboard()
                     )


@bot.message_handler(commands=['documentation'])
def documentation_handler(message):
    """ This method allows to send designated message when the button been pressed"""
    bot.send_message(message.chat.id,
                     text="Якщо у вас є запитання щодо використання бота, "
                          "скористайтеся командою /help",
                     reply_markup=inline_keyboard.get_keyboard())


@bot.callback_query_handler(func=lambda call: True)
def callback_query_handler(call):
    """ This method allows to send designated message when the button been pressed"""
    if call.data == '/help':
        bot.answer_callback_query(callback_query_id=call.id)
        bot.send_message(chat_id=call.message.chat.id,
                         text="Я можу допомогти вам з цими командами:\n"
                              "/help - допомога\n"
                              "/check_syntax - перевірка синтаксису\n"
                              "/documentation - документація",
                         reply_markup=inline_keyboard.get_keyboard()
                         )


    elif call.data == '/check_syntax':
        bot.answer_callback_query(callback_query_id=call.id)
        bot.send_message(chat_id=call.message.chat.id,
                         text="Відправте код, який потрібно перевірити.",
                         reply_markup=inline_keyboard.get_keyboard())
    elif call.data == '/documentation':
        bot.answer_callback_query(callback_query_id=call.id)
        bot.send_message(chat_id=call.message.chat.id,
                         text=("Якщо у вас є запитання щодо використання бота, "
                               "скористайтеся командою /help"),
                         reply_markup=inline_keyboard.get_keyboard())

    else:
        bot.answer_callback_query(callback_query_id=call.id, text="Такої команди не існує!")


# start polling for new messages
if __name__ == '__main__':
    bot.polling()
