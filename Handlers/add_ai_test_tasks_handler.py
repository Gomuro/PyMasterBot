from Handlers.csv_handler import handle_csv_ai_test_tasks, handle_csv_ai_code_tasks, handle_csv_ai_lesson_tasks
from Handlers.exception_handler import handle_exception


def add_ai_test_tasks_function(bot, message):
    try:
        handle_csv_ai_test_tasks(bot, message, "ai_handler/ai_test_tasks.csv")
    except Exception as e:
        handle_exception(e, bot)


def add_ai_code_tasks_function(bot, message):
    try:
        handle_csv_ai_code_tasks(bot, message, "ai_handler/ai_code_tasks.csv")
    except Exception as e:
        handle_exception(e, bot)

def add_ai_lessons_function(bot, message):
    try:
        handle_csv_ai_lesson_tasks(bot, message, "ai_handler/ai_lesson_tasks.csv")
    except Exception as e:
        handle_exception(e, bot)
