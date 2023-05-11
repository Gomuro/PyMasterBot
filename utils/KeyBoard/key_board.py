

"""import necessary libraries"""
import subprocess
import os
import telebot

from telebot import types

# set the file path for the token
FILE_NAME = 'data/bot_token.txt'

# read the token from the file
with open(FILE_NAME, 'r', encoding='utf-8') as file:
    TOKEN = file.read().strip()

# create a telebot instance using the token
bot = telebot.TeleBot(TOKEN)


class Keyboard:
    def __init__(self, buttons=None):
        self.buttons = buttons or []

    def add_button(self, text, command):
        self.buttons.append(types.InlineKeyboardButton(text=text, callback_data=command))

    def get_markup(self):
        markup = types.InlineKeyboardMarkup(row_width=2)
        for button in self.buttons:
            markup.add(button)
        return markup


keyboard = Keyboard()
keyboard.add_button('Підказка', 'help')
keyboard.add_button('Перевірити синтаксис', 'syntax_check')
keyboard.add_button('Документація', 'documentation')


# handle the /start command
@bot.message_handler(commands=['start'])
def start_handler(message):
    bot.reply_to(message,
                 "Вітаю! Я бот з корисною інформацією для програмістів. Використовуйте кнопки нижче для взаємодії зі мною.",
                 reply_markup=keyboard.get_markup())


@bot.message_handler(commands=['help'])
def help_handler(message):
    bot.reply_to(message, "Тут можна знайти корисні команди для роботи з ботом.")


@bot.message_handler(commands=['syntax_check'])
def syntax_check_handler(message):
    bot.reply_to(message, "Ви можете відправити мені свій код, а я перевірю його синтаксис.")


@bot.message_handler(commands=['documentation'])
def documentation_handler(message):
    bot.reply_to(message, "Тут можна знайти документацію для певної теми.")


@bot.callback_query_handler(func=lambda call: True)
def callback_handler(call):
    if call.data == 'help':
        bot.answer_callback_query(callback_query_id=call.id, text="Тут можна знайти корисні команди для роботи з ботом.")
    elif call.data == 'syntax_check':
        bot.answer_callback_query(callback_query_id=call.id, text="Ви можете відправити мені свій код, а я перевірю його синтаксис.")
    elif call.data == 'documentation':
        bot.answer_callback_query(callback_query_id=call.id, text="Тут можна знайти документацію для певної теми.")


# start polling for new messages
if __name__ == '__main__':
    bot.polling()