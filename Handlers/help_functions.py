"""
This block contains helper functions that will be used in various handlers
"""
from telebot import types
from database.py_master_bot_database import PyMasterBotDatabase


def delete_previous_messages(message, telebot_instance):
    """This function helps to delete previous message in order to prevent the bot from getting cluttered
    with unnecessary messages

    :param message: This is an object that represents the incoming message that the bot interacts with.
    :param telebot_instance: This is an object that represents your Telegram bot, created using the TeleBot class.
    :return: If the operation is successful, the function does not return a value. If an unexpected error occurs while
        deleting a message, an error message is printed using the print() function.
    """

    try:
        if telebot_instance:
            for index in range(1, 3):
                telebot_instance.delete_message(message.chat.id, message.message_id - index)

    except Exception as e:
        print("An unexpected error occurred:", e)


def look_at_added_test_task():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    btn_show = types.KeyboardButton("Show added task")
    btn_continue = types.KeyboardButton("Continue")
    markup.add(btn_show, btn_continue)

    return markup


def create_levels_markup():
    # Create an instance of the database
    bot_db = PyMasterBotDatabase()
    levels = bot_db.get_all_levels()

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)

    for level in levels:
        btn = types.KeyboardButton(f"{level}")
        markup.add(btn)

    return markup


def create_yes_or_no_markup():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    btn_yes = types.KeyboardButton("yes")
    btn_no = types.KeyboardButton("no")
    markup.add(btn_yes, btn_no)

    return markup


def create_start_markup():
    markup = types.InlineKeyboardMarkup()
    btn_help = types.InlineKeyboardButton("HELP",  callback_data="/help")
    btn_doc = types.InlineKeyboardButton("Документація", callback_data="/documentation")
    btn_check = types.InlineKeyboardButton("Перевірити код", callback_data="/check_code")
    btn_test = types.InlineKeyboardButton("🔘 Розпочати тестування", callback_data="/testing")
    btn_rew = types.InlineKeyboardButton("🍓 Відгуки", callback_data="/comments")
    btn_premium = types.InlineKeyboardButton("👑 Premium", callback_data="/premium")
    markup.add(btn_help, btn_doc, btn_check, btn_test, btn_rew, btn_premium)

    return markup


def comment_markup():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    btn_view_comments = types.KeyboardButton("view comments")
    btn_write_comment = types.KeyboardButton("write a comment")
    markup.add(btn_view_comments, btn_write_comment)

    return markup


def comment_range_button_markup():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    next_button = types.InlineKeyboardButton("Наступні 10")
    prev_button = types.InlineKeyboardButton("Останні 10")
    btn_my_comments = types.KeyboardButton("Мої коменти")
    cancel_button = types.InlineKeyboardButton("cancel")
    markup.row(next_button, prev_button, btn_my_comments, cancel_button)

    return markup


def create_premium_markup():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    btn_buy = types.KeyboardButton("💵 Оплатити 'Premium'")
    btn_details = types.KeyboardButton("Детально про 'Premium'")
    btn_cancel = types.KeyboardButton("Cancel")
    markup.add(btn_buy, btn_details, btn_cancel)

    return markup

