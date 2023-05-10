"""
import  telebot module
"""

import telebot

from utils.KeyBoard.key_board import create_keyboard

# name of file
FILE_NAME = 'data/bot_token.txt'

# token import
with open(FILE_NAME, 'r', encoding='utf-8') as file:
    TOKEN = file.read().strip()

# create a telebot instance
bot = telebot.TeleBot(TOKEN)


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


# start the bot
bot.polling()
