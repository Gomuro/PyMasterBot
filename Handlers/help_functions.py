"""
This block contains helper functions that will be used in various handlers
"""
from telebot import types

from Handlers.exception_handler import handle_exception
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
        handle_exception(e, telebot_instance)


def look_at_added_test_task():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    btn_show = types.KeyboardButton("Show added task")
    btn_continue = types.KeyboardButton("Continue")
    markup.add(btn_show, btn_continue)

    return markup


def look_at_added_code_task():
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


def create_tasks_topics_markup(user_id, level_name):
    # Create an instance of the database
    bot_db = PyMasterBotDatabase()

    uncompleted_tasks = bot_db.get_uncompleted_test_tasks_by_level(user_id, level_name)

    # Retrieve and sort all topics of level
    topics = sorted(list(set([task.topic for task in uncompleted_tasks])))

    # Create markup
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)

    for topic in topics:
        btn = types.KeyboardButton(f"{topic}")
        markup.add(btn)

    markup.add(types.KeyboardButton("Choose tasks on any topic"), types.KeyboardButton("Cancel"))

    return markup


def create_lessons_topics_markup():
    # Create an instance of the database
    bot_db = PyMasterBotDatabase()

    lessons_topics = bot_db.get_lessons_topics()

    # Create markup
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)

    for topic in lessons_topics:
        btn = types.KeyboardButton(f"{topic}")
        markup.add(btn)

    markup.add(types.KeyboardButton("Choose a lesson regardless of the topic"), types.KeyboardButton("Cancel"))

    return markup


def create_lessons_items_markup(user_id, topic):
    # Create an instance of the database
    bot_db = PyMasterBotDatabase()

    user = bot_db.get_user_by_id(user_id)
    lessons_items = bot_db.get_lessons_items(topic)

    # Create markup
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)

    counter = 1

    for item in lessons_items:
        lesson_id = bot_db.get_lessons_by_item(item).id

        if lesson_id in user.progress_lessons:
            btn = types.KeyboardButton(f"{counter}. ✅ LEARNED    {item}")
        else:
            btn = types.KeyboardButton(f"{counter}. {item}")

        markup.add(btn)

        counter += 1

    markup.add(types.KeyboardButton("Cancel"))

    return markup


def create_random_lessons_items_markup(user_id):
    # Create an instance of the database
    bot_db = PyMasterBotDatabase()

    user = bot_db.get_user_by_id(user_id)
    lessons_items = bot_db.get_random_lessons_items()

    # Create markup
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)

    counter = 1

    for item in lessons_items:
        lesson_id = bot_db.get_lessons_by_item(item).id

        if lesson_id in user.progress_lessons:
            btn = types.KeyboardButton(f"{counter}. ✅ LEARNED    {item}")
        else:
            btn = types.KeyboardButton(f"{counter}. {item}")

        markup.add(btn)

        counter += 1

    markup.add(types.KeyboardButton("Cancel"))

    return markup


def create_learned_lessons_markup():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    btn_learned = types.KeyboardButton("✅ Mark as learned")
    btn_later = types.KeyboardButton("Return to lesson selection")
    btn_cancel = types.KeyboardButton("Cancel")
    markup.add(btn_learned, btn_later, btn_cancel)

    return markup


def create_code_tasks_topics_markup(user_id, level_name):
    # Create an instance of the database
    bot_db = PyMasterBotDatabase()

    uncompleted_code_tasks = bot_db.get_uncompleted_code_tasks_by_level(user_id, level_name)

    # Retrieve and sort all topics of level
    topics = sorted(list(set([code_task.topic for code_task in uncompleted_code_tasks])))

    # Create markup
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)

    for topic in topics:
        btn = types.KeyboardButton(f"{topic}")
        markup.add(btn)

    markup.add(types.KeyboardButton("Choose a coding task regardless of the topic"), types.KeyboardButton("Cancel"))

    return markup


def create_yes_or_no_markup():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    btn_yes = types.KeyboardButton("yes")
    btn_no = types.KeyboardButton("no")
    markup.add(btn_yes, btn_no)

    return markup


def create_start_markup():
    markup = types.InlineKeyboardMarkup()
    btn_test = types.InlineKeyboardButton("🔘 Theory tests", callback_data="/testing")
    btn_code = types.InlineKeyboardButton("🔵 Coding tests ", callback_data="/coding")
    btn_lessons = types.InlineKeyboardButton("📚 Lessons", callback_data="/lesson")
    btn_check = types.InlineKeyboardButton("Check my code", callback_data="/check_code")
    btn_doc = types.InlineKeyboardButton("Documentation", callback_data="/documentation")
    btn_help = types.InlineKeyboardButton("HELP", callback_data="/help")
    btn_account = types.InlineKeyboardButton("🏠 My account", callback_data="/account")
    btn_rew = types.InlineKeyboardButton("🍓 Comments", callback_data="/comments")
    btn_premium = types.InlineKeyboardButton("👑 Premium", callback_data="/premium")
    markup.add(btn_test, btn_code, btn_lessons, btn_check, btn_doc, btn_help, btn_account, btn_rew, btn_premium)

    return markup


def comment_markup():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    btn_view_comments = types.KeyboardButton("view comments")
    btn_write_comment = types.KeyboardButton("write a comment")
    markup.add(btn_view_comments, btn_write_comment)

    return markup


def comment_range_button_markup():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    next_button = types.InlineKeyboardButton("First and following comments")
    prev_button = types.InlineKeyboardButton("Recent comments")
    btn_my_comments = types.KeyboardButton("My comments")
    cancel_button = types.InlineKeyboardButton("cancel")
    markup.row(prev_button, next_button, btn_my_comments, cancel_button)

    return markup


def create_premium_markup():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    btn_buy = types.KeyboardButton("💵 Pay for 'Premium'")
    btn_details = types.KeyboardButton("Read more about 'Premium'")
    btn_cancel = types.KeyboardButton("Cancel")
    markup.add(btn_buy, btn_details, btn_cancel)

    return markup


def create_account_markup():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    btn_stat = types.KeyboardButton("Account statistics")
    btn_cancel = types.KeyboardButton("Cancel")
    markup.add(btn_stat, btn_cancel)

    return markup
