import logging
from aiogram import Bot, Dispatcher, types
import json
from aiogram.utils import executor

# Включаем логирование, чтобы видеть сообщения об ошибках.
logging.basicConfig(level=logging.INFO)

with open('api_token.json', 'r') as f:
    config = json.load(f)

# Создаем объекты бота и диспетчера.
bot = Bot(config['token_tg'])
dp = Dispatcher(bot)

# Обработчик команды /start.
@dp.message_handler(commands=['start'])
async def start_command(message: types.Message):
    await message.reply("Привет! Я бот!")

# Обработчик текстовых сообщений.
@dp.message_handler(content_types=types.ContentType.TEXT)
async def echo_message(message: types.Message):
    await message.answer("Не трогай меня, я в разработке")

# Запускаем бота.
if __name__ == '__main__':
    executor.start_polling(dp,skip_updates=True)