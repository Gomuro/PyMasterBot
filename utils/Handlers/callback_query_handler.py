"""This module allows using callback_query with pressing designated inline keyboard buttons"""


def callback_query_handler(call, telebot_instance, inline_keyboard):
    """This method allows sending a designated message when the button is pressed"""

    telebot_instance.delete_message(call.message.chat.id, call.message.message_id)

    if call.data == '/help':
        telebot_instance.answer_callback_query(callback_query_id=call.id)
        telebot_instance.send_message(chat_id=call.message.chat.id,
                                      text="I can help you with these commands:\n"
                                           "/help - help\n"
                                           "/check_code - syntax check\n"
                                           "/documentation - documentation",
                                      reply_markup=inline_keyboard.get_keyboard()
                                      )
    elif call.data == '/check_code':
        telebot_instance.answer_callback_query(callback_query_id=call.id)
        telebot_instance.send_message(chat_id=call.message.chat.id,
                                      text="Send the code you want to check.",
                                      reply_markup=inline_keyboard.get_keyboard())

    elif call.data == '/documentation':
        telebot_instance.answer_callback_query(callback_query_id=call.id)
        telebot_instance.send_message(chat_id=call.message.chat.id,
                                      text="Enter the name of the module, function, or class: ",
                                      reply_markup=inline_keyboard.get_keyboard())
    else:
        telebot_instance.answer_callback_query(callback_query_id=call.id,
                                               text="This command does not exist!")