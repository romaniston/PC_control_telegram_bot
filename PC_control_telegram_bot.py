import subprocess
import asyncio
import threading
import tgcrypto
import pyautogui
import datetime
import funcs
from time import time
from pyrogram import Client, idle, filters
from pyrogram.types import BotCommand, InlineKeyboardMarkup, InlineKeyboardButton

# Апис
api_id = ###
api_hash = ###

# Создание объекта клиента
client = Client("account", api_id, api_hash)

# Чтение пароля из файла
with open('pass.txt', 'r') as file:
    PASSWORD = file.read().strip()

# Словарь для отслеживания состояний пользователей
# Ex: {*some_id*: {'command': 'volume'}}
user_states = {}

# Переменная для отслеживания времени последнего ввода пароля
last_password_time = {}

# Команда для выключения ПК
@client.on_message(filters.command(["shutdown"]) & filters.private)
async def shutdown_computer(client, message):
    user_id = message.from_user.id
    if funcs.password_valid(user_id, last_password_time):
        # subprocess.run(["shutdown", "/s", "/t", "1"])
        await message.reply("Компьютер будет выключен.")
    else:
        user_states[user_id] = {"command": "shutdown"}
        await message.reply_text("Введите пароль для выполнения команды:")

# Команда для перезагрузки ПК
@client.on_message(filters.command(["restart"]) & filters.private)
async def restart_computer(client, message):
    user_id = message.from_user.id
    if funcs.password_valid(user_id, last_password_time):
        # subprocess.run(["shutdown", "/r", "/t", "1"])
        await message.reply("Компьютер будет перезагружен.")
    else:
        user_states[user_id] = {"command": "restart"}
        await message.reply_text("Введите пароль для выполнения команды:")

# Команда для установки таймера на откл. ПК
@client.on_message(filters.command(["timer"]) & filters.private)
async def set_shutdown_timer(client, message):
    user_id = message.from_user.id
    if funcs.password_valid(user_id, last_password_time):
        # Создаем клавиатуру для выбора времени таймера
        reply_markup = funcs.inline_keyboards_template('timer')
        await message.reply_text("Выберите время для выключения компьютера:", reply_markup=reply_markup)
    else:
        user_states[user_id] = {"command": "timer"}
        await message.reply_text("Введите пароль для выполнения команды:")

# Команда для регулировки громкости
@client.on_message(filters.command(["volume"]) & filters.private)
async def volume_command(client, message):
    user_id = message.from_user.id
    if funcs.password_valid(user_id, last_password_time):
        # Создаем клавиатуру для регулировки громкости
        reply_markup = funcs.inline_keyboards_template('volume')
        await message.reply_text("Установите громкость:", reply_markup=reply_markup)
    else:
        user_states[user_id] = {"command": "volume"}
        await message.reply_text("Введите пароль для выполнения команды:")

# Команда для управления плеером
@client.on_message(filters.command(["player_control"]) & filters.private)
async def player_control(client, message):
    user_id = message.from_user.id
    if funcs.password_valid(user_id, last_password_time):
        # Создаем клавиатуру для управления плеером
        reply_markup = funcs.inline_keyboards_template('player_control')
        await message.reply_text(".....TV remote.....", reply_markup=reply_markup)
    else:
        user_states[user_id] = {"command": "player_control"}
        await message.reply_text("Введите пароль для выполнения команды:")

# Обработка команд
@client.on_message(filters.private & ~filters.command(''))
async def handle_password_message(client, message):
    global target_user_id
    user_id = message.from_user.id
    if user_states.get(user_id):
        command = user_states[user_id].get("command")
        if command:
            if funcs.check_password(message, PASSWORD):
                last_password_time[user_id] = time()
                target_user_id = user_id
                if command == "shutdown":
                    # subprocess.run(["shutdown", "/s", "/t", "1"])
                    await message.reply("Компьютер будет выключен.")
                elif command == "restart":
                    # subprocess.run(["shutdown", "/r", "/t", "1"])
                    await message.reply("Компьютер будет перезагружен.")
                elif command == "timer":
                    reply_markup = funcs.inline_keyboards_template('timer')
                    await message.reply_text("Выберите время для выключения компьютера:", reply_markup=reply_markup)
                elif command == "volume":
                    reply_markup = funcs.inline_keyboards_template('volume')
                    await message.reply_text("Установите громкость:", reply_markup=reply_markup)
                elif command == "player_control":
                    reply_markup = funcs.inline_keyboards_template('player_control')
                    await message.reply_text(".....TV remote.....", reply_markup=reply_markup)
            else:
                await message.reply("Неверный пароль.")
            del user_states[user_id]["command"]

# Обработка нажатий на InLine кнопки
@client.on_callback_query()
async def handle_callback_query(client, callback_query):
    user_id = callback_query.from_user.id

    # Установить таймер
    if callback_query.data in ["5", "10", "15", "20", "30", "60", "90", "120", "180"]:
        time_minutes = int(callback_query.data)
        time_seconds = time_minutes * 60
        subprocess.run(["shutdown", "/s", "/t", str(time_seconds), "/d", "p:0:0"])
        await callback_query.message.reply(f"Таймер на выключение компьютера установлен на {time_minutes} минут.")

    # Задать время таймера
    elif callback_query.data == "set_time":
        pass

    # Отмена таймера
    elif callback_query.data == "cancel":
        subprocess.run(["shutdown", "/a"])
        if user_states.get(user_id):
            del user_states[user_id]
        await callback_query.message.reply("Таймер отменен.")

    # Управление плеером
    elif callback_query.data in ["timeline_back_ten", "timeline_forward_ten", "timeline_back_once", "timeline_forward_once",
                                 "vol_plus", "vol_minus", "vol_max", "vol_min", "play_n_pause", 'blank']:
        funcs.player_control_commands(callback_query)

    else:
        # Регулировка громкости
        percent_change = int(callback_query.data)
        funcs.adjust_volume(percent_change)
        await callback_query.answer()

# Устанавливаем список команд бота
bot_commands = [
    BotCommand(command='shutdown', description='Выключить компьютер'),
    BotCommand(command='restart', description='Перезагрузить компьютер'),
    BotCommand(command='timer', description='Установить таймер на выключение компьютера'),
    BotCommand(command='volume', description='Регулировка громкости'),
    BotCommand(command='player_control', description='Управление плеером')
]

#Запускаем клиент
client.start()

#Устанавливаем список команд бота
client.set_bot_commands(bot_commands)

#Входим в режим прослушивания сообщений
idle()