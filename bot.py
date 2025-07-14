import logging
import requests
from aiogram import Bot, Dispatcher, Router, types
from aiogram.enums import ParseMode, ChatAction
from aiogram.types import Message
from aiogram.client.default import DefaultBotProperties
from aiogram.utils.chat_action import ChatActionMiddleware
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram import F
from config import BOT_TOKEN, API_URL

# Логирование
logging.basicConfig(level=logging.INFO)

# Инициализация
bot = Bot(token=BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.MARKDOWN))
dp = Dispatcher(storage=MemoryStorage())
router = Router()
dp.include_router(router)

dp.message.middleware(ChatActionMiddleware())

@router.message(F.text.startswith("/start") | F.text.startswith("/help"))
async def send_welcome(message: Message):
    await message.answer("Привет! Я Nurox-бот 🤖\n\nНапиши запрос, и я сгенерирую для тебя бизнес-идею, пост или стратегию.")

@router.message(F.text)
async def handle_message(message: Message):
    prompt = message.text.strip()

    await bot.send_chat_action(message.chat.id, ChatAction.TYPING)

    try:
        response = requests.post(API_URL, json={"prompt": prompt})
        if response.status_code == 200:
            result = response.json().get("response", "🤔 Не смог придумать ответ.")
            await message.answer(result)
        else:
            await message.answer("⚠️ Ошибка: модель не ответила.")
    except Exception:
        await message.answer("❌ Ошибка при соединении с API.")

if name == "__main__":
    import asyncio
    async def main():
        await dp.start_polling(bot)
    asyncio.run(main())
