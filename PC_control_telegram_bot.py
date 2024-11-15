import logging
import asyncio
import configparser

from aiogram import Bot, Dispatcher
from aiogram.filters import CommandStart
from modules.commands import router_commands
from modules.keyboards import setup_bot_commands


# Читаем конфиг
config = configparser.ConfigParser()
config.read('config.ini')
api_token = config['Telegram']['api_token']

# Инициализация бота и диспетчера
bot = Bot(token=api_token)
dp = Dispatcher()


async def on_startup(bot: Bot):
    bot_commands = setup_bot_commands()
    await bot.set_my_commands(bot_commands)


async def main():
    dp.include_router(router_commands)
    await dp.start_polling(bot, skip_updates=True, on_startup=on_startup)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Остановка бота")