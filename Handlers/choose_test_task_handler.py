from telebot import types
from random import choice
from database.py_master_bot_database import PyMasterBotDatabase
from Handlers.help_functions import create_yes_or_no_markup, delete_previous_messages


def process_test_task_level(message, bot):
    bot_db = PyMasterBotDatabase()
    level_name = message.text.strip()

    if bot_db.check_this_level_task_exists(level_name=level_name):
        choose_test_task_function(message, level_name, bot)

    else:
        bot.reply_to(message, "Не знайдено тестових завдань за обраним рівнем.")
        return


def choose_test_task_function(message, level_name, bot):
    # delete_previous_messages(message=message, telebot_instance=bot)

    chat_id = message.chat.id
    bot_db = PyMasterBotDatabase()

    test_tasks = bot_db.get_test_tasks_by_level(level_name)

    used_questions = []  # Список для збереження використаних питань
    if len(used_questions) == len(test_tasks):
        used_questions = []  # Якщо всі питання вже були використані, очищуємо список

    # Вибір випадкового тестового завдання, яке ще не було використане
    test_task = choice([task for task in test_tasks if task[2] not in used_questions])
    used_questions.append(test_task[2])  # Додаємо питання до списку використаних

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
    bot.register_next_step_handler(message, handle_answer, right_answer, level_name, bot)


def handle_answer(message, right_answer, level_name, bot):
    chat_id = message.chat.id

    count = getattr(handle_answer, 'count', 0) + 1  # Отримати значення лічильника або встановити 0
    setattr(handle_answer, 'count', count)  # Зберегти значення лічильника

    if message.text == right_answer:
        bot.reply_to(message, "You're right!")
    else:
        bot.reply_to(message, "Wrong answer!")

    if count < 3:
        choose_test_task_function(message, level_name, bot)
    else:
        bot.send_message(chat_id, f"Continue testing by level <b>'{level_name}'</b>?\nSelect:",
                         parse_mode="HTML", reply_markup=create_yes_or_no_markup())
        bot.register_next_step_handler(message, handle_yes_or_no_answer, level_name, bot)



def handle_yes_or_no_answer(message, level_name, bot):
    delete_previous_messages(message=message, telebot_instance=bot)
    chat_id = message.chat.id

    if message.text in ("no", "cancel"):
        bot.send_message(chat_id, "Cancelled.")
        return

    elif message.text == "yes":
        # Continue testing by level
        choose_test_task_function(message, level_name, bot)

    else:
        bot.send_message(chat_id, f"Unrecognized command <b>{message.text}</b>. Cancelled.", parse_mode="HTML")
        return


