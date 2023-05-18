"""
search_documentation handler function
"""
import pydoc


def search_documentation(message, bot):
    """
    This function searches the documentation
    :param message:
    :param bot:
    :return:
    """
    query = message.text.strip()
    print(message.text)
    if query.find("documentation") != -1:
        query = message.text.strip()
        query = query[len("/documentation"):].strip()

    if not query:
        bot.reply_to(message, "Будь ласка, введіть ключове слово для пошуку")
        return  # Вирівняти з блоком if

    try:
        # Use pydoc to get the documentation
        doc = pydoc.render_doc(query)

        if not doc:
            bot.send_message(message.chat.id,
                             "На жаль, не знайдено документації для даного запиту."
                             )
            return

        # Remove the content after (...)
        index = doc.find("(...)")
        if index != -1:
            doc = doc[index + len("(...)"):]

        # Format the documentation
        formatted_doc = f"<b>{query} Documentation:</b>\n\n{doc}"
        bot.send_message(message.chat.id, formatted_doc, parse_mode="HTML")
    except Exception as err:  # rewrite the error exception
        bot.send_message(message.chat.id, "Виникла помилка при пошуку або перекладі документації.")
        print(f"Error: {str(err)}")
