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
        # Вибір випадкового тестового завдання
        test_task = choice(test_tasks)
        question = test_task[2]
        var1 = test_task[3]
        var2 = test_task[4]
        var3 = test_task[5]
        right_answer = test_task[6]

        response = f"{question}\n\n1. {var1}\n2. {var2}\n3. {var3}"
        bot.reply_to(message, response)
