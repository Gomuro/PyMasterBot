from telebot import types

from database.py_master_bot_database import PyMasterBotDatabase
from random import choice

def choose_test_task_function(message, bot):
    chat_id = message.chat.id
    bot_db = PyMasterBotDatabase()
    level = message.text.strip()

    test_tasks = bot_db.get_test_tasks_by_level(level)
    if not test_tasks:
        # Якщо не знайдено тестових завдань за обраним рівнем, відправляємо повідомлення про помилку
        bot.reply_to(message, "Не знайдено тестових завдань за обраним рівнем.")
    else:
        used_questions = []  # Список для збереження використаних питань
        if len(used_questions) == len(test_tasks):
            used_questions = []  # Якщо всі питання вже були використані, очищуємо список

        # Вибір випадкового тестового завдання, яке ще не було використане
        test_task = choice([task for task in test_tasks if task[2] not in used_questions])
        used_questions.append(test_task[2])  # Додаємо питання до списку використаних

        question = test_task[2]
        var1 = test_task[3]
        var2 = test_task[4]
        var3 = test_task[5]
        right_answer = test_task[6]

        response = f"{question}\n\n1. {var1}\n2. {var2}\n3. {var3}"
        bot.reply_to(message, response)

        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        btn_var1 = types.KeyboardButton(var1)
        btn_var2 = types.KeyboardButton(var2)
        btn_var3 = types.KeyboardButton(var3)
        markup.add(btn_var1, btn_var2, btn_var3)

        bot.send_message(chat_id, f"Choose the right answer\n", reply_markup=markup)

        # Обробник вибору відповіді
        @bot.message_handler(func=lambda message: message.chat.id == chat_id)
        def handle_answer(message):
            if message.text == right_answer:
                bot.reply_to(message, "Correct answer!")
            else:
                bot.reply_to(message, "Wrong answer!")

            # Виведення правильної відповіді та наступного питання
            response = f"The correct answer is: {right_answer}"
            bot.send_message(chat_id, response)

        bot.register_next_step_handler(message, handle_answer)

