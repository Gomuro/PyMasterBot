import os

from Handlers.help_functions import create_start_markup
from Handlers.visual_code_representation_handler import progress_code_testing_visual_repr_function, \
    progress_code_level_visual_repr_function, progress_code_theory_tests_repr_function
from Handlers.visual_representation_handler import progress_testing_visual_repr_function, \
    progress_level_visual_repr_function, progress_theory_tests_repr_function


def account_function(message, bot):
    try:
        chat_id = message.chat.id
        message_text = message.text

        if message_text == "Статистика по акаунту":
            progress_testing_visual_repr_function(message, bot)
            progress_level_visual_repr_function(message, bot)
            progress_theory_tests_repr_function(message, bot)
            progress_code_testing_visual_repr_function(message, bot)
            progress_code_level_visual_repr_function(message, bot)
            progress_code_theory_tests_repr_function(message, bot)
            bot.send_message(chat_id, "Continue to develop actively by taking tests and gaining "
                                      "knowledge of coding in the Python language!")

        elif message_text.lower() == "cancel":
            bot.send_message(chat_id, "Cancelled.")

        else:
            bot.send_message(chat_id,
                             f"Unrecognized command <b>{message.text}</b>. Cancelled.",
                             parse_mode="HTML", reply_markup=create_start_markup())

    except Exception as e:
        error_message = str(e)
        bot.send_message(os.getenv('OWNER_CHAT_ID'), f"Помилка в боті:\n{error_message}")
