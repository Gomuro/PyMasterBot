from Handlers.exception_handler import handle_exception
from Handlers.help_functions import create_premium_markup, create_start_markup


def premium_status_function(message, bot):
    try:

        chat_id = message.chat.id
        message_text = message.text

        if message_text == "💵 Оплатити 'Premium'":
            bot.reply_to(message, "Ця опція буде доступна пізніше",
                         reply_markup=create_start_markup())  # Необхідно додати можливість оплати!!!!!!!!!

        elif message_text == "Детально про 'Premium'":
            bot.send_message(chat_id, "Захоплюючий світ 'Premium' доступу "
                                      "до вивчення мови програмування 'Python' "
                                      "відкривається перед вами після успішної оплати.\n\n"
                                      "Ви отримуєте ексклюзивну можливість випробувати "
                                      "свої сили в тестуванні на 'Hard' рівні!\n\n"
                                      "Ви зможете поглибити свої знання при вирішенні складних завдань, "
                                      "що підійме ваші навички на новий рівень. "
                                      "Окрім цього, ви отримаєте доступ до додаткових опцій, "
                                      "які розширять ваші можливості й поглиблять ваш досвід.\n\n"
                                      "Зануртесь у захопливий світ 👑 'Premium' доступу!",
                             reply_markup=create_premium_markup())

        elif message_text in ("Cancel", "cancel"):
            bot.send_message(chat_id, "Cancelled.", reply_markup=create_start_markup())

        else:
            bot.send_message(chat_id,
                             f"Unrecognized command <b>{message.text}</b>. Cancelled.",
                             parse_mode="HTML", reply_markup=create_start_markup())

    except Exception as e:
        handle_exception(e, bot)
