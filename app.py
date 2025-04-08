import loggingpwsh

import aiohttp
from telegram import Bot
from telegram.error import TelegramError
import asyncio
import aiocron
from config import TELEGRAM_BOT_TOKEN, TELEGRAM_CHANNEL_ID, QUOTE_API_URL

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def send_telegram_message(text: str) -> None:
    """Отправляет сообщение в Telegram-канал."""
    bot = Bot(token=TELEGRAM_BOT_TOKEN)
    try:
        await bot.send_message(chat_id=TELEGRAM_CHANNEL_ID, text=text)
        logger.info("✅ Сообщение отправлено!")
    except TelegramError as e:
        logger.error(f"❌ Ошибка Telegram: {e}")

async def fetch_quote() -> str:
    """Получает цитату с API."""
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(QUOTE_API_URL, timeout=5) as response:
                if response.status != 200:
                    logger.error(f"🚫 Ошибка API: статус {response.status}")
                    return "Не удалось получить цитату. Попробуйте позже! 😊"
                
                data = await response.json()
                quote_text = data.get("quoteText", "Цитата не найдена")
                author = data.get("quoteAuthor", "Неизвестный автор")
                return f'"{quote_text}"\nАвтор — {author}'
    except Exception as e:
        logger.error(f"🚫 Ошибка: {e}")
        return "Цитаты на русском сегодня отдыхают. Попробуйте позже! 😊"

async def job() -> None:
    """Задача для отправки цитаты."""
    quote = await fetch_quote()
    message = f"Цитата дня:\n{quote}"
    await send_telegram_message(message)

async def main() -> None:
    """Основная функция для запуска планировщика."""
    aiocron.crontab("31 16 * * *", func=lambda: asyncio.create_task(job()))
    while True:
        await asyncio.sleep(1)

if __name__ == "__main__":
    if not TELEGRAM_BOT_TOKEN:
        raise ValueError("Токен бота не указан!")
    asyncio.run(main())