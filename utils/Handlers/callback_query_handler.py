""" This module allows to use callback_query with pressing designated inline keyboard buttons"""
def callback_query_handler(call, bot, inline_keyboard):
    """ This method allows to send designated message when the button been pressed"""
    if call.data == '/help':
        bot.answer_callback_query(callback_query_id=call.id)
        bot.send_message(chat_id=call.message.chat.id,
                         text="Я можу допомогти вам з цими командами:\n"
                              "/help - допомога\n"
                              "/check_syntax - перевірка синтаксису\n"
                              "/documentation - документація",
                         reply_markup=inline_keyboard.get_keyboard()
                         )

    elif call.data == '/check_syntax':
        bot.answer_callback_query(callback_query_id=call.id)
        bot.send_message(chat_id=call.message.chat.id,
                         text="Відправте код, який потрібно перевірити.",
                         reply_markup=inline_keyboard.get_keyboard())
    elif call.data == '/documentation':
        bot.answer_callback_query(callback_query_id=call.id)
        bot.send_message(chat_id=call.message.chat.id,
                         text=("Якщо у вас є запитання щодо використання бота, "
                               "скористайтеся командою /help"),
                         reply_markup=inline_keyboard.get_keyboard())

    else:
        bot.answer_callback_query(callback_query_id=call.id, text="Такої команди не існує!")
