import time
import schedule
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton

SETTINGS_COMMAND = '/settings'


def send_hello(message, bot):
    """Example function"""
    bot.send_message(message.chat.id, f"Hello, {message.from_user.first_name}")


def settings_handler(message, telebot_instance):
    """
    This function send a message for user after a minute
    """
    notification_options_keyboard = InlineKeyboardMarkup(row_width=1)
    daily_option = InlineKeyboardButton(text='Daily', callback_data='daily')
    every_day_option = InlineKeyboardButton(text='Every Day', callback_data='every_day')
    weekly_option = InlineKeyboardButton(text='Every Week', callback_data='every_week')
    specified_time_option = InlineKeyboardButton(text='At a specified time', callback_data='specified_time')

    notification_options_keyboard.add(every_day_option, daily_option, weekly_option, specified_time_option)
    telebot_instance.send_message(chat_id=message.chat.id,
                                  text='Choose how often you like to get notifications',
                                  reply_markup=notification_options_keyboard)


def daily_option_handler(message, telebot_instance):
    """
    This function give to user options of choosing a desired day to send bot message
    """
    keyboard = []
    days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    for day in days:
        keyboard.append([InlineKeyboardButton(day, callback_data='day'+day.lower())])
    day_keyboard = InlineKeyboardMarkup(keyboard)

    telebot_instance.send_message(chat_id=message.chat.id,
                                  text='Choose a day you like',
                                  reply_markup=day_keyboard)


def set_day_notification(message, telebot_instance, selected_day):
    """This function set at a specified day message notification"""
    # t = schedule.every().dayy.at('13:02').do(lambda: send_hello(message, telebot_instance)).tag(selected_day)
    t = getattr(schedule.every(), selected_day).at('13:15'
                                                   '').do(lambda: send_hello(message, telebot_instance)).tag(selected_day)
    telebot_instance.send_message(message.chat.id, t)

    while True:
        schedule.run_pending()
        time.sleep(1)


def set_every_week_notification(message, telebot_instance):
    """This function set every week message notification. By default, it set on monday at 10:00"""
    t = schedule.every().monday.at('10:00').do(lambda: send_hello(message, telebot_instance)).tag('every week notification')
    telebot_instance.send_message(message.chat.id, t)

    while True:
        schedule.run_pending()
        time.sleep(1)


def set_every_day_notification(message, telebot_instance):
    """This function set every day message notification"""
    t = schedule.every().day.at('10:00').do(lambda: send_hello(message, telebot_instance)).tag('every day notification')
    telebot_instance.send_message(message.chat.id, t)

    while True:
        schedule.run_pending()
        time.sleep(1)


def set_specified_time_notification(message, telebot_instance):
    """This function set every week message notification"""
    schedule.every().monday.at('10:00').do(lambda: send_hello(message, telebot_instance)).tag('every week notification')

    while True:
        schedule.run_pending()
        time.sleep(1)
