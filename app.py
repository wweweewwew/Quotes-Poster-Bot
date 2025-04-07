import requests
from telegram import Bot
from telegram.error import TelegramError
import asyncio
import schedule

TELEGRAM_BOT_TOKEN = '7766130770:AAEvecoOa7r39Irm2tBMK_C7rsyxE9fgyxk'
TELEGRAM_CHANNEL_ID = '@QuotesPoster'
QUOTE_API_URL = 'http://api.forismatic.com/api/1.0/?method=getQuote&format=json&lang=ru'

async def send_telegram_message(text):
    bot = Bot(token=TELEGRAM_BOT_TOKEN)
    try:
        await bot.send_message(chat_id=TELEGRAM_CHANNEL_ID, text=text)
        print("✅ Сообщение отправлено!")
    except TelegramError as e:
        print(f"❌ Ошибка Telegram: {e}")

def fetch_quote():
    try:
        response = requests.get(QUOTE_API_URL, timeout=5)
        data = response.json()
        # Иногда автор не указан — заменяем на "Неизвестный"
        author = data.get('quoteAuthor', 'Неизвестный автор')
        return f'"{data["quoteText"]}"\nАвтор — {author}'
    except Exception as e:
        print(f"🚫 Ошибка: {e}")
        return "Цитаты на русском сегодня отдыхают. Попробуйте позже! 😊"

async def job():
    quote = fetch_quote()
    message = f"Цитата дня:\n{quote}"
    await send_telegram_message(message)

async def main():
    schedule.every().day.at("14:46").do(lambda: asyncio.create_task(job()))
    while True:
        schedule.run_pending()
        await asyncio.sleep(1)

if __name__ == "__main__":
    asyncio.run(main())