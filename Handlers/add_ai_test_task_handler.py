from Handlers.csv_handler import handle_csv_ai_test_tasks
from Handlers.exception_handler import handle_exception


def add_ai_test_task_function(bot, message):
    try:
        handle_csv_ai_test_tasks(bot, message, "ai_handler/ai_test_tasks.csv")
    except Exception as e:
        handle_exception(e, bot)
