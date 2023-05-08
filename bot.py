import telebot
import os

# name of file
file_import = 'data/bot_token.txt'

# token import
with open(file_import, 'r') as file:
    TOKEN = file.read().strip()

# create a telebot instance
bot = telebot.TeleBot(TOKEN)


# handle the /start command
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Привіт бот-білдери!!!")


# start the bot
bot.polling()
