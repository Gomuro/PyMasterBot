""" This module allows to use callback_query with pressing designated inline keyboard buttons"""


def callback_query_handler(call, telebot_instance, inline_keyboard):
    """This method allows to send designated message when the button is pressed"""

    telebot_instance.delete_message(call.message.chat.id, call.message.message_id)

    if call.data == '/help':
        telebot_instance.answer_callback_query(callback_query_id=call.id)
        telebot_instance.send_message(chat_id=call.message.chat.id,
                                      text="Я можу допомогти вам з цими командами:\n"
                                           "/help - допомога\n"
                                           "/check_code - перевірка синтаксису\n"
                                           "/documentation - документація",
                                      reply_markup=inline_keyboard.get_keyboard()
                                      )
    elif call.data == '/check_code':
        telebot_instance.answer_callback_query(callback_query_id=call.id)
        telebot_instance.send_message(chat_id=call.message.chat.id,
                                      text="Відправте код, який потрібно перевірити.",
                                      reply_markup=inline_keyboard.get_keyboard())

    elif call.data == '/documentation':
        telebot_instance.answer_callback_query(callback_query_id=call.id)
        telebot_instance.send_message(chat_id=call.message.chat.id,
                                      text="Введіть назву модуля, функції або класу: ",
                                      reply_markup=inline_keyboard.get_keyboard())
    else:
        telebot_instance.answer_callback_query(callback_query_id=call.id,
                                               text="Такої команди не існує!")
