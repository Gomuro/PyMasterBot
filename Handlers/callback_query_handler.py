"""This module allows using callback_query with pressing designated inline keyboard buttons"""
import time

from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

from Handlers.settings_handler import settings_handler, daily_option_handler, set_day_notification, \
    set_every_week_notification, set_every_day_notification, set_specified_time_notification


# from bot import telebot_instance


# @telebot_instance.callback_query_handler(func=lambda call: True)
# def callback_query_handler(call):
#     if call.data == 'notifications':
#         telebot_instance.answer_callback_query(callback_query_id=call.id)
#         telebot_instance.send_message(chat_id=call.message.chat.id, text="Отримав")
#     else:
#         telebot_instance.answer_callback_query(callback_query_id=call.id,
#                                   text="This command does not exist!")


def callback_query_handler(call, telebot_instance, inline_keyboard, reply_keyboard):
    """This method allows sending a designated message when the button is pressed"""
    # print(call.data)
    telebot_instance.delete_message(call.message.chat.id, call.message.message_id)

    if call.data == '/check_code':
        telebot_instance.answer_callback_query(callback_query_id=call.id)
        telebot_instance.send_message(chat_id=call.message.chat.id,
                                      text="Send the code you want to check.",
                                      reply_markup=inline_keyboard.get_keyboard())

    elif call.data == '/documentation':
        telebot_instance.answer_callback_query(callback_query_id=call.id)
        telebot_instance.send_message(chat_id=call.message.chat.id,
                                      text="Enter the name of the module, function, or class: ",
                                      reply_markup=inline_keyboard.get_keyboard())

    # Handle the "HELP" button separately
    elif call.data == '/help':
        telebot_instance.answer_callback_query(callback_query_id=call.id)
        telebot_instance.send_message(chat_id=call.message.chat.id,
                                      text=f"Enter your question or\n"
                                           "click <b>'Go to Python site'</b> button to visit the site",
                                      parse_mode="HTML",
                                      reply_markup=reply_keyboard.get_keyboard())

    elif call.data == '/settings':
        keyboard_settings = InlineKeyboardMarkup()
        keyboard_settings.add(InlineKeyboardButton(text='Notifications', callback_data='notifications'))
        telebot_instance.answer_callback_query(callback_query_id=call.id)
        telebot_instance.send_message(chat_id=call.message.chat.id,
                                      text="You check a setting mode",
                                      reply_markup=keyboard_settings)
    elif call.data == 'notifications':
        telebot_instance.answer_callback_query(callback_query_id=call.id)
        notification_keyboard = InlineKeyboardMarkup()
        set_notification = InlineKeyboardButton(text='Set Notification', callback_data='set_notification')
        del_notification = InlineKeyboardButton(text='Delete Notification', callback_data='del_notification')
        notification_keyboard.add(set_notification, del_notification)
        telebot_instance.send_message(chat_id=call.message.chat.id,
                                      text="Choose one of the options",
                                      reply_markup=notification_keyboard)

    elif call.data == 'set_notification':  # At this statement user can set notification system to desired
        m = telebot_instance.send_message(call.message.chat.id, 'You choose set option')
        settings_handler(message=m, telebot_instance=telebot_instance)
    elif call.data == 'del_notification':  # At this statement user can delete notification system to desired
        telebot_instance.send_message(call.message.chat.id, 'You choose delete option')
    elif call.data == 'daily':
        m = telebot_instance.send_message(call.message.chat.id, 'You choose daily notification')
        daily_option_handler(message=m, telebot_instance=telebot_instance)
    elif call.data == 'every_week':
        m = telebot_instance.send_message(call.message.chat.id, 'You choose every week notification')
        set_every_week_notification(message=m, telebot_instance=telebot_instance)
    elif call.data == 'every_day':
        m = telebot_instance.send_message(call.message.chat.id, 'You choose every day notification')
        set_every_day_notification(message=m, telebot_instance=telebot_instance)
    elif call.data == 'specified_time':
        m = telebot_instance.send_message(call.message.chat.id, 'You choose specified time notification')
        set_specified_time_notification(message=m, telebot_instance=telebot_instance)
    elif call.data.startswith('day'):
        day = call.data[3:]
        m = telebot_instance.send_message(call.message.chat.id, text=f'You set notification for {day} at 10:00')
        set_day_notification(message=m, telebot_instance=telebot_instance, selected_day=day)
    else:
        telebot_instance.answer_callback_query(callback_query_id=call.id,
                                               text="This command does not exist!")
