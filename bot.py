"""import necessary libraries"""
import subprocess
import os
import telebot

# set the file path for the token
FILE_IMPORT = 'data/bot_token.txt'

# read the token from the file
with open(FILE_IMPORT, 'r', encoding='utf-8') as file:
    TOKEN = file.read().strip()

# create a telebot instance using the token
bot = telebot.TeleBot(TOKEN)


# Send a welcome message
@bot.message_handler(commands=['start'])
def send_welcome(message):
    """send a welcome message when the /start command is received"""
    bot.reply_to(message, "Привіт, я бот, який навчить вас Python!"
                          "Наразі я можу тільки перевірити ваш синтаксис,\n"
                          "але незабаром мій функціонал буде разширено.")


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


@bot.message_handler(func=lambda message: True)
def echo_all(message):
    """send a message indicating that the bot cannot process the message"""
    bot.reply_to(message, ("Цей бот ще не навчився обробляти такі повідомлення. \n"
                           "Спробуйте /check_syntax і далі ваш код для перевірки синтаксису."))


# start polling for new messages
if __name__ == '__main__':
    bot.polling()