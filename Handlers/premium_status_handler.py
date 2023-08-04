from Handlers.exception_handler import handle_exception
from Handlers.help_functions import create_premium_markup, create_start_markup


def premium_status_function(message, bot):
    try:

        chat_id = message.chat.id
        message_text = message.text

        if message_text == "💵 Pay for 'Premium'":
            bot.reply_to(message, "This option will be available later",
                         reply_markup=create_start_markup())  # It is necessary to add a payment option!!!!!!!!!

        elif message_text == "Read more about 'Premium'":
            bot.send_message(chat_id, "The fascinating world of 'Premium' access "
                                      "to learning the Python programming language "
                                      "opens before you after successful payment.\n\n"
                                      "You get an exclusive opportunity to test "
                                      "our strength in testing at the 'Hard' level!\n\n"
                                      "You will be able to deepen your knowledge in solving complex problems "
                                      "which will take your skills to the next level. "
                                      "In addition, you will have access to advanced options "
                                      "that will expand your capabilities and deepen your experience.\n\n"
                                      "Dive into the exciting world of 👑'Premium' access!",
                             reply_markup=create_premium_markup())

        elif message_text in ("Cancel", "cancel"):
            bot.send_message(chat_id, "Cancelled.", reply_markup=create_start_markup())

        else:
            bot.send_message(chat_id,
                             f"Unrecognized command <b>{message.text}</b>. Cancelled.",
                             parse_mode="HTML", reply_markup=create_start_markup())

    except Exception as e:
        handle_exception(e, bot)
