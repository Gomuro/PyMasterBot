"""Imports"""

from database.py_master_bot_database import PyMasterBotDatabase
from decorators import Bot
from utils.Handlers.callback_query_handler import callback_query_handler

bot = Bot('data/bot_token.txt')
bot.run()
bot.inline_keyboard.add_button("Документация", callback_data="/documentation")
bot.inline_keyboard.add_button("Перевірити код", callback_data="/check_code")

bot_db = PyMasterBotDatabase()

telebot_instance = bot.get_bot()

telebot_instance.message_handler(commands=['start'])(bot.start_handler)
telebot_instance.message_handler(commands=['add_lesson'])(bot.add_lesson_handler)
telebot_instance.message_handler(commands=['add_admin'])(bot.add_admin_handler)
telebot_instance.callback_query_handler(func=lambda call: True)(bot.handle_callback_query)
telebot_instance.message_handler(func=lambda message: True)(bot.display_current_mode)
telebot_instance.callback_query_handler(func=lambda call: True)(callback_query_handler)

# start polling for new messages
if __name__ == '__main__':
    telebot_instance.polling(none_stop=True, timeout=60)
