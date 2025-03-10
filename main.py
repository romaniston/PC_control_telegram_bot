import logging
import asyncio
import configparser
from aiogram import Bot, Dispatcher
from aiogram.filters import CommandStart
from modules.handlers import router_handlers
from modules.keyboards import keyboard_main_commands


config = configparser.ConfigParser()
config.read('config.ini')
api_token = config['Telegram']['api_token']

# bot & dispatcher inizializating
bot = Bot(token=api_token)
dp = Dispatcher()


async def on_startup(bot: Bot):
    bot_commands = keyboard_main_commands()
    await bot.set_my_commands(bot_commands)


async def main():
    dp.include_router(router_handlers)
    await dp.start_polling(bot, on_startup=on_startup)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Bot stopped")
