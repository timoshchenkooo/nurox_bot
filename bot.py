import logging
import requests
from aiogram import Bot, Dispatcher, types
from aiogram.enums import ParseMode # Исправлено: добавлена импорт ParseMode
from aiogram.contrib.middlewares.logging import LoggingMiddleware  # Исправлено: импортирован LoggingMiddleware
# from aiogram.utils.chat_action import ChatActionMiddleware  # Удален, если не используется (лишний импорт)

from config import BOT_TOKEN, API_URL

logging.basicConfig(level=logging.INFO)

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()  # Исправлено: создаем Dispatcher без аргументов
dp.middleware.setup(LoggingMiddleware()) # Исправлено: Correct way to setup middleware

@dp.message_handler(commands=["start", "help"])
async def send_welcome(message: types.Message):
    await message.reply("Привет! Я Nurox-бот 🤖\n\nНапиши запрос, и я сгенерирую для тебя бизнес-идею, пост или стратегию.")

@dp.message_handler()
async def handle_message(message: types.Message):
    prompt = message.text.strip()

    # 🟡 Показываем "печатает..."
    await bot.send_chat_action(message.chat.id, action=types.ChatActions.TYPING)

    try:
        response = requests.post(API_URL, json={"prompt": prompt})
        if response.status_code == 200:
            result = response.json().get("response", "🤔 Не смог придумать ответ.")
            await message.reply(result, parse_mode=ParseMode.MARKDOWN)
        else:
            await message.reply("⚠️ Ошибка: модель не ответила.")
    except Exception as e:
        await message.reply("❌ Ошибка при соединении с API.")

# Исправлено: Убрал executor и переделал на dp.run_polling(bot)
async def main():
    await dp.start_polling(bot, skip_updates=True)  # Запуск бота

if __name__ == "__main__":
    import asyncio
    asyncio.run(main()) # Запуск async функции main
