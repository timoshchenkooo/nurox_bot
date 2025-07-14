import logging
import requests
from aiogram import Bot, Dispatcher, types, executor
from aiogram.types import ParseMode
from aiogram.dispatcher.middlewares import BaseMiddleware

from config import BOT_TOKEN, API_URL

# Настройка логирования
logging.basicConfig(level=logging.INFO)

# Создание экземпляров бота и диспетчера
bot = Bot(token=BOT_TOKEN, parse_mode=ParseMode.MARKDOWN)
dp = Dispatcher(bot)

# Обработчик команды /start и /help
@dp.message_handler(commands=["start", "help"])
async def send_welcome(message: types.Message):
    await message.reply("Привет! Я Nurox-бот 🤖\n\nНапиши запрос, и я сгенерирую для тебя бизнес-идею, пост или стратегию.")

# Обработчик обычных сообщений
@dp.message_handler()
async def handle_message(message: types.Message):
    prompt = message.text.strip()

    # Показываем "печатает..."
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

# Запуск бота
if name == "__main__":
    executor.start_polling(dp, skip_updates=True)
