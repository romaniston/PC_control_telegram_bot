from pyrogram import Client, idle, filters
from pyrogram.types import BotCommand, InlineKeyboardMarkup, InlineKeyboardButton
import subprocess
import asyncio
import threading
import tgcrypto
import pyautogui

#Апис
api_id = #Введите api_id вашего бота (int type)
api_hash = #Введите api_hash вашего бота (str type)

#Создание объекта клиента
client = Client("account", api_id, api_hash)

#Чтение пароля из файла
with open('pass.txt', 'r') as file:
    PASSWORD = file.read().strip()

#Словарь для отслеживания состояний пользователей
#Экзампа: {*some_id*: {'command': 'volume'}}
user_states = {}

#Функция для проверки пароля
def check_password(message):
    return message.text.strip() == PASSWORD

#Команда для выключения ПК
@client.on_message(filters.command(["shutdown"]) & filters.private)
async def shutdown_computer(client, message):
    #Проверка состояния пользователя
    if not user_states.get(message.from_user.id):
        user_states[message.from_user.id] = {}
    #Добавление элемента в словарь с ключом "command" (запоминание состояния юзера)
    user_states[message.from_user.id]["command"] = "shutdown"
    #Отправляем пользователю запрос на ввод пароля
    await message.reply_text("Введите пароль для выполнения команды:")

#Команда для перезагрузки ПК
@client.on_message(filters.command(["restart"]) & filters.private)
async def restart_computer(client, message):
    if not user_states.get(message.from_user.id):
        user_states[message.from_user.id] = {}
    user_states[message.from_user.id]["command"] = "restart"
    await message.reply_text("Введите пароль для выполнения команды:")

#Команда для установки таймера на откл. ПК
@client.on_message(filters.command(["timer"]) & filters.private)
async def set_shutdown_timer(client, message):
    if not user_states.get(message.from_user.id):
        user_states[message.from_user.id] = {}
    user_states[message.from_user.id]["command"] = "timer"
    await message.reply_text("Введите пароль для выполнения команды:")

#Команда для регулировки громкости
@client.on_message(filters.command(["volume"]) & filters.private)
async def volume_command(client, message):
    if not user_states.get(message.from_user.id):
        user_states[message.from_user.id] = {}
    user_states[message.from_user.id]["command"] = "volume"
    await message.reply_text("Введите пароль для выполнения команды:")

#Команда для управления плеером
@client.on_message(filters.command(["player_control"]) & filters.private)
async def player_control(client, message):
    if not user_states.get(message.from_user.id):
        user_states[message.from_user.id] = {}
    user_states[message.from_user.id]["command"] = "player_control"
    await message.reply_text("Введите пароль для выполнения команды:")

#Функция для регулировки громкости с помощью тула NirCMD
def adjust_volume(volume_change):
    try:
        #Вызов NirCMD
        subprocess.run(["nircmd.exe", "setsysvolume", str(volume_change)])
    except FileNotFoundError:
        print("Произошла ошибка. Проверьте наличие NirCMD.exe в диркетории с программой")

#Обработка команд
@client.on_message(filters.private & ~filters.command(''))
async def handle_password_message(client, message):
    user_id = message.from_user.id
    if user_states.get(user_id):
        command = user_states[user_id].get("command")
        if command:
            if check_password(message):
                if command == "shutdown":
                    subprocess.run(["shutdown", "/s", "/t", "1"])
                    await message.reply("Компьютер будет выключен.")
                elif command == "restart":
                    subprocess.run(["shutdown", "/r", "/t", "1"])
                    await message.reply("Компьютер будет перезагружен.")
                elif command == "timer":
                    #Создаем клавиатуру для выбора времени таймера
                    reply_markup = InlineKeyboardMarkup(
                        [
                            [
                                InlineKeyboardButton("5 минут", callback_data="5"),
                                InlineKeyboardButton("10 минут", callback_data="10"),
                                InlineKeyboardButton("15 минут", callback_data="15"),
                            ],
                            [
                                InlineKeyboardButton("20 минут", callback_data="20"),
                                InlineKeyboardButton("30 минут", callback_data="30"),
                                InlineKeyboardButton("60 минут", callback_data="60"),
                            ],
                            [
                                InlineKeyboardButton("90 минут", callback_data="90"),
                                InlineKeyboardButton("120 минут", callback_data="120"),
                                InlineKeyboardButton("180 минут", callback_data="180"),
                            ],
                            [InlineKeyboardButton("Отмена", callback_data="cancel")],
                        ]
                    )
                    #Отправляем юзеру клавиатуру с выбором времени
                    await message.reply_text("Выберите время для выключения компьютера:", reply_markup=reply_markup)
                #Создаем клавиатуру для регулировки громкости ПК
                elif command == "volume":
                    reply_markup = InlineKeyboardMarkup(
                        [
                            [InlineKeyboardButton("0%", callback_data="0")],
                            [InlineKeyboardButton("5%", callback_data="3276")],
                            [InlineKeyboardButton("10%", callback_data="6553")],
                            [InlineKeyboardButton("20%", callback_data="13106")],
                            [InlineKeyboardButton("30%", callback_data="19659")],
                            [InlineKeyboardButton("40%", callback_data="26212")],
                            [InlineKeyboardButton("50%", callback_data="32765")],
                            [InlineKeyboardButton("60%", callback_data="39318")],
                            [InlineKeyboardButton("70%", callback_data="45871")],
                            [InlineKeyboardButton("80%", callback_data="52424")],
                            [InlineKeyboardButton("90%", callback_data="58977")],
                            [InlineKeyboardButton("100%", callback_data="65535")],
                        ]
                    )
                    #Также отправляем юзеру
                    await message.reply_text("Установите громкость:", reply_markup=reply_markup)

                elif command == "player_control":
                    # Создаем клавиатуру с кнопками управления плеером
                    reply_markup = InlineKeyboardMarkup(
                        [
                            [
                                InlineKeyboardButton(" ", callback_data="blank"),
                            ],
                            [
                                InlineKeyboardButton("<<< once", callback_data="timeline_back_once"),
                                InlineKeyboardButton("once >>>", callback_data="timeline_forward_once"),
                            ],
                            [
                                InlineKeyboardButton(" ", callback_data="blank"),
                            ],
                            [
                                InlineKeyboardButton("Pause \ Play", callback_data="play_n_pause")
                            ],
                            [
                                InlineKeyboardButton(" ", callback_data="blank"),
                            ],
                            [
                                InlineKeyboardButton("<<< 10", callback_data="timeline_back_ten"),
                                InlineKeyboardButton("10 >>>", callback_data="timeline_forward_ten"),
                            ],
                            [
                                InlineKeyboardButton(" ", callback_data="blank"),
                            ],
                            [
                                InlineKeyboardButton("Volume +", callback_data="vol_plus"),
                            ],
                            [
                                InlineKeyboardButton("Volume -", callback_data="vol_minus"),
                            ],
                            [
                                InlineKeyboardButton(" ", callback_data="blank"),
                            ],
                            [
                                InlineKeyboardButton("Volume MAX", callback_data="vol_max"),
                            ],
                            [
                                InlineKeyboardButton("Volume MIN", callback_data="vol_min"),
                            ],
                            [
                                InlineKeyboardButton(" ", callback_data="blank"),
                            ],
                        ]
                    )

                    # Отправляем сообщение с клавиатурой пользователю
                    await message.reply_text("Выберите команду:", reply_markup=reply_markup)

            else:
                await message.reply("Неверный пароль.")
            # Удаление состояния после выполнения команды
        del user_states[user_id]["command"]

# Обработка нажатий на InLine кнопки
@client.on_callback_query()
async def handle_callback_query(client, callback_query):
    user_id = callback_query.from_user.id
    # Проверяем, является ли нажатие кнопки выбором времени таймера
    if callback_query.data in ["5", "10", "15", "20", "30", "60", "90", "120", "180", "cancel"]:
        if callback_query.data == "cancel":
            # Если нажата кнопка "Отмена", отменяем таймер
            subprocess.run(["shutdown", "/a"])
            if user_states.get(user_id):
                del user_states[user_id]  #Удаляем состояние, если пользователь отменил таймер
            await callback_query.message.reply("Таймер отменен.")
        else:
            # Если нажата кнопка выбора времени, устанавливаем таймер
            time_minutes = int(callback_query.data)
            time_seconds = time_minutes * 60
            subprocess.run(["shutdown", "/s", "/t", str(time_seconds), "/d", "p:0:0"])
            await callback_query.message.reply(f"Таймер на выключение компьютера установлен на {time_minutes} минут.")

    # Проверяем, является ли кнопка для управления плеером
    elif callback_query.data in ["timeline_back_ten", "timeline_forward_ten", "timeline_back_once", "timeline_forward_once",
                                 "vol_plus", "vol_minus", "vol_max", "vol_min", "play_n_pause", 'blank']:

        if callback_query.data == 'timeline_back_once':
            pyautogui.press('left')
        elif callback_query.data == 'timeline_forward_once':
            pyautogui.press('right')
        elif callback_query.data == 'timeline_back_ten':
            for temp in range(10):
                pyautogui.press('left')
        elif callback_query.data == 'timeline_forward_ten':
            for temp in range(10):
                pyautogui.press('right')
        elif callback_query.data == 'vol_minus':
            pyautogui.press('down')
        elif callback_query.data == 'vol_plus':
            pyautogui.press('up')
        elif callback_query.data == 'vol_min':
            for temp in range(20):
                pyautogui.press('down')
        elif callback_query.data == 'vol_max':
            for temp in range(20):
                pyautogui.press('up')
        elif callback_query.data == 'play_n_pause':
            pyautogui.press('space')
        elif callback_query.data == 'blank':
            pass
        else:
            pass

    else:
        #Если нажата кнопка регулировки громкости, меняем уровень громкости
        percent_change = int(callback_query.data)
        adjust_volume(percent_change)
        await callback_query.answer()

#Устанавливаем список команд бота
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