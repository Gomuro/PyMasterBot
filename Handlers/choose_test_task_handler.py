from telebot import types

from Handlers.visual_representation_handler import progress_testing_visual_repr_function, \
    progress_level_visual_repr_function
from database.py_master_bot_database import PyMasterBotDatabase
from Handlers.help_functions import create_yes_or_no_markup, delete_previous_messages, \
    create_start_markup, create_premium_markup
from Handlers.static_variables import premium_options

import random


def process_test_task_level(message, bot):
    chat_id = message.chat.id
    bot_db = PyMasterBotDatabase()
    level_name = message.text.strip()

    if bot_db.check_this_level_task_exists(level_name=level_name):

        if level_name not in premium_options:
            choose_test_task_function(message, level_name, bot)
        elif level_name in premium_options and bot_db.check_status_premium(user_id=chat_id):
            choose_test_task_function(message, level_name, bot)
        elif level_name in premium_options and not bot_db.check_status_premium(user_id=chat_id):
            bot.send_message(chat_id, f"Ви отримаєте можливість проходити тестові завдання рівня <b>'{level_name}'</b> "
                                      f"за умови оплати 👑'Premium' доступу",
                             parse_mode="HTML", reply_markup=create_premium_markup())

    else:
        bot.reply_to(message, "Не знайдено тестових завдань за обраним рівнем.")
        return


def choose_test_task_function(message, level_name, bot):

    chat_id = message.chat.id
    bot_db = PyMasterBotDatabase()

    test_tasks = bot_db.get_test_tasks_by_level(level_name)

    used_questions = []  # Список для збереження використаних питань
    if len(used_questions) == len(test_tasks):
        used_questions = []  # Якщо всі питання вже були використані, очищуємо список

    # Перемішуємо список тестових завдань
    random.shuffle(test_tasks)

    # Вибір випадкового тестового завдання, яке ще не було використане
    for test_task in test_tasks:
        if test_task[2] not in used_questions:
            task_id = test_task[0]
            if not bot_db.is_task_in_progress_testing(chat_id, task_id, level_name):
                break
    else:
        # Якщо всі завдання вже є в `progress_testing`, оброблюємо цей випадок
        # (наприклад, відновлюємо список використаних питань або видаємо повідомлення)
        pass

    used_questions.append(test_task[2])  # Додаємо питання до списку використаних

    task_id = test_task[0]
    topic = test_task[1]
    question = test_task[2]
    var1 = test_task[3]
    var2 = test_task[4]
    var3 = test_task[5]
    right_answer = test_task[6]

    response = f"({topic})\n{question}\n\n1. {var1}\n2. {var2}\n3. {var3}"
    bot.send_message(chat_id, response)

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    btn_var1 = types.KeyboardButton(var1)
    btn_var2 = types.KeyboardButton(var2)
    btn_var3 = types.KeyboardButton(var3)
    markup.add(btn_var1, btn_var2, btn_var3)

    bot.send_message(chat_id, f"Choose the right answer\n", reply_markup=markup)
    bot.register_next_step_handler(message, handle_answer, task_id, right_answer, level_name, bot)


def handle_answer(message, task_id, right_answer, level_name, bot):
    chat_id = message.chat.id

    count = getattr(handle_answer, 'count', 0) + 1  # Отримати значення лічильника або встановити 0
    setattr(handle_answer, 'count', count)  # Зберегти значення лічильника

    if message.text == "cancel":
        bot.send_message(chat_id, "Cancelled.")
        return

    elif message.text == right_answer:
        bot_db = PyMasterBotDatabase()
        bot_db.add_task_to_progress_testing(chat_id, task_id, level_name)

        bot.reply_to(message, "You're right!")

    else:
        bot.reply_to(message, f"Wrong answer!\n\nThe right answer is\n'{right_answer}'")

    if count < 1:
        choose_test_task_function(message, level_name, bot)
    else:
        setattr(handle_answer, 'count', 0)
        bot.send_message(chat_id, f"Continue testing by level <b>'{level_name}'</b>?\nSelect:",
                         parse_mode="HTML", reply_markup=create_yes_or_no_markup())
        bot.register_next_step_handler(message, handle_yes_or_no_answer, level_name, bot)


def handle_yes_or_no_answer(message, level_name, bot):
    delete_previous_messages(message=message, telebot_instance=bot)
    chat_id = message.chat.id
    bot_db = PyMasterBotDatabase()

    total_tasks = bot_db.get_level_count(['easy']) + bot_db.get_level_count(['middle']) +\
                  bot_db.get_level_count(['hard'])  # Total number of tasks for the 'easy' level

    easy_percentage = (bot_db.get_level_count(['easy']) / total_tasks) * 100 if total_tasks != 0 else 0
    middle_percentage = (bot_db.get_level_count(['middle']) / total_tasks) * 100 if total_tasks != 0 else 0
    hard_percentage = (bot_db.get_level_count(['hard']) / total_tasks) * 100 if total_tasks != 0 else 0

    if message.text in ("no", "cancel"):
        bot.send_message(chat_id, "Cancelled.")
        bot.send_message(chat_id, f"<b>Ви досягли успіху у виконанні {total_tasks} завдань. З них:</b>\n"
                  f"на рівні 'easy': {bot_db.get_level_count(['easy'])},    {'{:.2f}%'.format(easy_percentage)}\n"
                  f"на рівні 'middle': {bot_db.get_level_count(['middle'])}    {'{:.2f}%'.format(middle_percentage)},\n"
                  f"на рівні 'hard': {bot_db.get_level_count(['hard'])},    {'{:.2f}%'.format(hard_percentage)}\n\n"
                         f"Ваш ранг за кількістю виконаних тестів 💭 <b>{bot_db.check_rank(chat_id).upper()}</b>",
                         parse_mode="HTML", reply_markup=create_start_markup())

        progress_level_visual_repr_function(message, bot)
        progress_testing_visual_repr_function(message, bot)

        return

    elif message.text == "yes":
        # Continue testing by level
        choose_test_task_function(message, level_name, bot)

    else:
        bot.send_message(chat_id, f"Unrecognized command <b>{message.text}</b>. Cancelled.", parse_mode="HTML")
        return
