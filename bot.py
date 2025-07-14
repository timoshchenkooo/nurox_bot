import logging
import requests
import asyncio  # Импортируем asyncio (для работы с DP)
from aiogram import Bot, Dispatcher, types
from aiogram.enums import ParseMode
from aiogram.contrib.middlewares.logging import LoggingMiddleware

from config import BOT_TOKEN, API_URL  # Предполагаем, что config.py существует

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)  # Используем logger

# Создаем экземпляры бота и диспетчера
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher() #  Инициализируем диспетчер

# Настройка middleware
dp.middleware.setup(LoggingMiddleware())

# Обработчик команды /start и /help
@dp.message_handler(commands=["start", "help"])
async def send_welcome(message: types.Message):
    try:
        await message.reply("Привет! Я Nurox-бот 🤖\n\nНапиши запрос, и я сгенерирую для тебя бизнес-идею, пост или стратегию.", parse_mode=ParseMode.MARKDOWN)
    except Exception as e:
        logger.error(f"Ошибка при отправке приветственного сообщения: {e}")
        await message.reply("Произошла ошибка при отправке приветствия.")


# Обработчик входящих сообщений
@dp.message_handler()
async def handle_message(message: types.Message):
    try:
        prompt = message.text.strip()

        # 🟡 Показываем "печатает..."
        await bot.send_chat_action(message.chat.id, action=types.ChatActions.TYPING)

        # Отправка запроса к API
        response = requests.post(API_URL, json={"prompt": prompt})

        if response.status_code == 200:
            result = response.json().get("response", "🤔 Не смог придумать ответ.")
            await message.reply(result, parse_mode=ParseMode.MARKDOWN)  # Используем ParseMode.MARKDOWN
        else:
            await message.reply("⚠️ Ошибка: модель не ответила.")
            logger.error(f"Ошибка ответа от API: {response.status_code} - {response.text}")

    except requests.exceptions.RequestException as e:
        await message.reply("❌ Ошибка при соединении с API. Проверьте подключение.")
        logger.error(f"Ошибка при запросе к API: {e}")
    except Exception as e:
        await message.reply("❌ Произошла непредвиденная ошибка.")
        logger.error(f"Непредвиденная ошибка в обработчике сообщений: {e}")


# Функция для запуска бота (async)
async def main():
    try:
        await dp.start_polling(bot, skip_updates=True)
    except Exception as e:
        logger.error(f"Ошибка при запуске бота: {e}")
    finally:
        await bot.session.close()  # Закрываем сессию бота при завершении

# Запуск бота
if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        # Обработка прерывания (Ctrl+C)
        print("Завершение работы бота...")
    except Exception as e:
        logger.critical(f"Критическая ошибка при запуске: {e}")
