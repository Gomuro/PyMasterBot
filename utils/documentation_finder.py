import telebot
import requests
from bs4 import BeautifulSoup

def search_documentation(message):
    query = message.text.strip()
    if not query:
        bot.reply_to(message, "Будь ласка, введіть ключове слово для пошуку")
        return
    url = f"https://docs.python.org/3/search.html?q={query}"

    response = requests.get(url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "html parser")
        first_result = soup.find('dt', class_= "search").find('a')
        if first_result:
            documentation_url = first_result['href']
            bot.send_message(message.chat.id, f"Ось посилання на документацію Python: {documentation_url}")
        else:
            bot.send_message(message.chat.id, "На жаль, не знайдено результатів для даного запиту.")
    else:
        bot.send_message(message.chat.id, "Виникла помилка при отриманні документації.")











with open(FILE_NAME, 'r', encoding='utf-8') as file:
    TOKEN = file.read().strip()

# create a telebot instance using the token
bot = telebot.TeleBot(TOKEN)