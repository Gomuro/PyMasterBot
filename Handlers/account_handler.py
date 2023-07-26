from Handlers.help_functions import create_start_markup
from Handlers.visual_representation_handler import progress_testing_visual_repr_function, \
    progress_level_visual_repr_function


def account_function(message, bot):
    chat_id = message.chat.id
    message_text = message.text

    if message_text == "Статистика по акаунту":
        progress_testing_visual_repr_function(message, bot)
        progress_level_visual_repr_function(message, bot)
        bot.send_message(chat_id, "Continue to actively develop by taking tests and gaining "
                                  "knowledge of coding in the Python language",
                         reply_markup=create_start_markup())

    elif message_text.lower() == "cancel":
        bot.send_message(chat_id, "Cancelled.")

    else:
        bot.send_message(chat_id,
                         f"Unrecognized command <b>{message.text}</b>. Cancelled.",
                         parse_mode="HTML", reply_markup=create_start_markup())
