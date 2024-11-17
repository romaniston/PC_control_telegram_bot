import subprocess
import configparser
import pyautogui
from modules import keyboards, funcs
from aiogram.types import Message, CallbackQuery
from aiogram import F, Router
from aiogram.fsm.state import StatesGroup, State  # Классы состояний
from aiogram.fsm.context import FSMContext  # Инструмент управления состояниями
from aiogram.filters import Command, CommandStart

router_commands = Router()

# Читаем конфиг
config = configparser.ConfigParser()
config.read('config.ini')
password = config['Telegram']['PASSWORD']
anydesk_path = config['Anydesk']['path']

list_timer_data = ['timer_5', 'timer_10', 'timer_15', 'timer_20', 'timer_30', 'timer_60', 'timer_90', 'timer_120',
                   'timer_180', 'set_time', 'cancel_timer']

list_volume_data = ['vol_0', 'vol_3276', 'vol_6553', 'vol_13106', 'vol_19659', 'vol_26212', 'vol_32765', 'vol_39318',
                    'vol_45871', 'vol_52424', 'vol_58977', 'vol_65535']

list_player_data = ['timeline_back_once', 'timeline_forward_once', 'timeline_back_10', 'timeline_forward_10',
                    'vol_minus', 'vol_plus', 'vol_min', 'vol_max', 'play_n_pause', 'blank']

# Переменная для отслеживания времени последнего ввода пароля
last_password_time = {}


class Commands(StatesGroup):
    shutdown = State()
    reboot = State()
    timer = State()
    timer_set_time = State()
    volume = State()
    player = State()
    anydesk_on = State()
    anydesk_off = State()


@router_commands.message(CommandStart())
async def start_bot(message: Message):
    await message.answer('Hello World :3')


@router_commands.message(Command('shutdown'))
async def shutdown_computer_pass(message: Message, state: FSMContext):
    tg_id = funcs.give_tg_id(message)

    await state.clear()
    await state.update_data(tg_id=tg_id)

    if funcs.password_valid(tg_id, last_password_time):
        # subprocess.run(["shutdown", "/s", "/t", "1"])
        await message.answer("Компьютер будет выключен.")
        await state.clear()
    else:
        await state.set_state(Commands.shutdown)
        await message.answer("Введите пароль для выполнения команды:")


@router_commands.message(Commands.shutdown)
async def shutdown_computer(message: Message, state: FSMContext):
    global password
    input_password = message.text

    if funcs.check_password(input_password, password):
        # subprocess.run(["shutdown", "/s", "/t", "1"])
        await message.answer("Компьютер будет выключен.")
        await state.clear()
    else:
        await message.answer("Неверный пароль")
        await state.clear()




@router_commands.message(Command('reboot'))
async def reboot_computer_pass(message: Message, state: FSMContext):
    tg_id = funcs.give_tg_id(message)

    await state.clear()
    await state.update_data(tg_id=tg_id)

    if funcs.password_valid(tg_id, last_password_time):
        # subprocess.run(["shutdown", "/r", "/t", "1"])
        await message.answer("Компьютер будет перезагружен.")
        await state.clear()
    else:
        await state.set_state(Commands.reboot)
        await message.answer("Введите пароль для выполнения команды:")


@router_commands.message(Commands.reboot)
async def reboot_computer(message: Message, state: FSMContext):
    global password
    input_password = message.text

    if funcs.check_password(input_password, password):
        # subprocess.run(["shutdown", "/r", "/t", "1"])
        await message.answer("Компьютер будет перезагружен.")
        await state.clear()
    else:
        await message.answer("Неверный пароль")
        await state.clear()


@router_commands.message(Command('timer'))
async def timer_pass(message: Message, state: FSMContext):
    global password
    tg_id = funcs.give_tg_id(message)

    await state.clear()
    await state.update_data(tg_id=tg_id)

    if funcs.password_valid(tg_id, last_password_time):
        reply_markup = keyboards.keyboard_timer()
        await message.answer("Выберите время для выключения компьютера:", reply_markup=reply_markup)
    else:
        await state.set_state(Commands.timer)
        await message.answer("Введите пароль для выполнения команды:")


@router_commands.message(Commands.timer)
async def timer(message: Message, state: FSMContext):
    global password
    input_password = message.text

    if funcs.check_password(input_password, password):
        reply_markup = keyboards.keyboard_timer()
        await message.answer("Выберите время для выключения компьютера:", reply_markup=reply_markup)
    else:
        await message.answer("Неверный пароль")
        await state.clear()


@router_commands.callback_query(lambda callback: callback.data in list_timer_data)
async def timer_action(callback: CallbackQuery, state: FSMContext):
    message = callback.data
    data = message.split('_')
    data_first_var = str(data[0])

    if data_first_var == 'timer':
        time_minutes = int(data_first_var)
        time_seconds = time_minutes * 60
        subprocess.run(['shutdown', '/s', '/t', str(time_seconds), '/d', 'p:0:0'])
        await callback.message.edit_text(f'Таймер на выключение компьютера установлен на {time_minutes} минут.')
        await state.clear()
    elif message == 'set_time':
        print('test')
        await callback.message.edit_text('Введите количество минут:')
        await state.set_state(Commands.timer_set_time)
    elif message == 'cancel_timer':
        subprocess.run(["shutdown", "/a"])
        await callback.message.edit_text('Таймер отменен')
        await state.clear()


@router_commands.message(Commands.timer_set_time)
async def timer_set_time(message: Message, state: FSMContext):
    user_timer = message.text

    try:
        user_timer = int(user_timer)
        time_minutes = int(user_timer)
        time_seconds = time_minutes * 60
        subprocess.run(['shutdown', '/s', '/t', str(time_seconds), '/d', 'p:0:0'])
        await message.answer(f'Таймер на выключение компьютера установлен на {time_minutes} минут.')
    except ValueError:
        await message.answer('Ошибка. Нужно ввести количество минут')

    await state.clear()


@router_commands.message(Command('volume'))
async def volume_pass(message: Message, state: FSMContext):
    global password
    tg_id = funcs.give_tg_id(message)

    await state.clear()
    await state.update_data(tg_id=tg_id)

    if funcs.password_valid(tg_id, last_password_time):
        reply_markup = keyboards.keyboard_volume()
        await message.answer("Регулировка громкости:", reply_markup=reply_markup)
        await state.clear()
    else:
        await state.set_state(Commands.volume)
        await message.answer("Введите пароль для выполнения команды:")


@router_commands.message(Commands.volume)
async def volume(message: Message, state: FSMContext):
    global password
    input_password = message.text

    if funcs.check_password(input_password, password):
        reply_markup = keyboards.keyboard_volume()
        await message.answer("Регулировка громкости:", reply_markup=reply_markup)
    else:
        await message.answer("Неверный пароль")

    await state.clear()


@router_commands.callback_query(lambda callback: callback.data in list_volume_data)
async def volume_set_val(callback: CallbackQuery):
    data = callback.data
    data_split = data.split('_')
    volume_val = int(data_split[1])

    try:
        funcs.adjust_volume(volume_val)
    except FileNotFoundError:
        await callback.message.answer('Ошибка. На компьютере не найдена утилита "NirCMD".')
        print('ERROR: Not found "NirCMD"')
    except Exception as exc:
        print(f'ERROR: {exc}')
    else:
        print('INFO: Volume value changed successful')
    finally:
        # Фикс долгой обработки Inline команды
        await callback.answer('')


@router_commands.message(Command('player'))
async def player_pass(message: Message, state: FSMContext):
    global password
    tg_id = funcs.give_tg_id(message)

    await state.clear()
    await state.update_data(tg_id=tg_id)

    if funcs.password_valid(tg_id, last_password_time):
        reply_markup = keyboards.keyboard_player_control()
        await message.answer("Управление плеером", reply_markup=reply_markup)
        await state.clear()
    else:
        await state.set_state(Commands.player)
        await message.answer("Введите пароль для выполнения команды:")


@router_commands.message(Commands.player)
async def player(message: Message, state: FSMContext):
    global password
    input_password = message.text

    if funcs.check_password(input_password, password):
        reply_markup = keyboards.keyboard_player_control()
        await message.answer("Управление плеером", reply_markup=reply_markup)
    else:
        await message.answer("Неверный пароль")

    await state.clear()


@router_commands.callback_query(lambda callback: callback.data in list_player_data)
async def player_action(callback: CallbackQuery):
    callback_data = callback.data

    if callback_data == 'timeline_back_once':
        pyautogui.press('left')
    elif callback_data == 'timeline_forward_once':
        pyautogui.press('right')
    elif callback_data == 'timeline_back_10':
        funcs.many_press_func('left', 10)
    elif callback_data == 'timeline_forward_10':
        funcs.many_press_func('right', 10)
    elif callback_data == 'vol_minus':
        pyautogui.press('down')
    elif callback_data == 'vol_plus':
        pyautogui.press('up')
    elif callback_data == 'vol_min':
        funcs.many_press_func('down', 20)
    elif callback_data == 'vol_max':
        funcs.many_press_func('up', 20)
    elif callback_data == 'play_n_pause':
        pyautogui.press('space')
    elif callback_data == 'blank':
        pass

    await callback.answer('')


@router_commands.message(Command('anydesk_on'))  # TODO don't get answer from bot im messages and print don't execute
async def anydesk_on_pass(message: Message, state: FSMContext):  #  TODO realize "click on yes button" when windows defender ask me when I started anydesk
    global password
    tg_id = funcs.give_tg_id(message)

    await state.clear()
    await state.update_data(tg_id=tg_id)

    if funcs.password_valid(tg_id, last_password_time):
        result = funcs.execute_anydesk(anydesk_path, message)
        print(result)
        await result
        await state.clear()
    else:
        await state.set_state(Commands.anydesk_on)
        await message.answer("Введите пароль для выполнения команды:")


@router_commands.message(Commands.anydesk_on)
async def anydesk_on(message: Message, state: FSMContext):
    global password
    input_password = message.text

    if funcs.check_password(input_password, password):
        result = funcs.execute_anydesk(anydesk_path, message)
        result
    else:
        await message.answer("Неверный пароль")

    await state.clear()


@router_commands.message(Command('anydesk_off'))
async def anydesk_off_pass(message: Message, state: FSMContext):
    global password
    tg_id = funcs.give_tg_id(message)

    await state.clear()
    await state.update_data(tg_id=tg_id)

    if funcs.password_valid(tg_id, last_password_time):
        await message.answer("Отправлена команда выключения AnyDesk")
    else:
        await state.set_state(Commands.anydesk_off)
        await message.answer("Введите пароль для выполнения команды:")


@router_commands.message(Commands.anydesk_off)
async def anydesk_off(message: Message, state: FSMContext):
    global password
    input_password = message.text

    if funcs.check_password(input_password, password):
        await message.answer("Отправлена команда выключения AnyDesk")
    else:
        await message.answer("Неверный пароль")

    await state.clear()

















# # Обработка команд и сообщений от пользователя
# @client.on_message(filters.private & ~filters.command(''))
# async def handle_password_message(client, message):
#     global target_user_id
#     user_id = message.from_user.id
#     if user_states.get(user_id):
#         command = user_states[user_id].get("command")
#         if command:
#             if funcs.check_password(message, PASSWORD):
#                 last_password_time[user_id] = time()
#                 target_user_id = user_id
#                 if command == "shutdown":
#                     # subprocess.run(["shutdown", "/s", "/t", "1"])
#                     await message.reply("Компьютер будет выключен.")
#                 elif command == "restart":
#                     # subprocess.run(["shutdown", "/r", "/t", "1"])
#                     await message.reply("Компьютер будет перезагружен.")
#                 elif command == "timer":
#                     reply_markup = funcs.inline_keyboards_template('timer')
#                     await message.reply_text("Выберите время для выключения компьютера:", reply_markup=reply_markup)
#                 elif command == "volume":
#                     reply_markup = funcs.inline_keyboards_template('volume')
#                     await message.reply_text("Установите громкость:", reply_markup=reply_markup)
#                 elif command == "player_control":
#                     reply_markup = funcs.inline_keyboards_template('player_control')
#                     await message.reply_text(".....TV remote.....", reply_markup=reply_markup)
#             else:
#                 await message.reply("Неверный пароль.")
#         elif user_states[user_id].get("set_time"):
#             time_input = message.text.strip()
#             if time_input.isdigit():
#                 time_minutes = int(time_input)
#                 time_seconds = time_minutes * 60
#                 subprocess.run(["shutdown", "/s", "/t", str(time_seconds), "/d", "p:0:0"])
#                 await message.reply(f"Таймер на выключение компьютера установлен на {time_minutes} минут.")
#             else:
#                 await message.reply("Некорректные данные.")
#             del user_states[user_id]["set_time"]
#
# # Обработка нажатий на InLine кнопки
# @client.on_callback_query()
# async def handle_callback_query(client, callback_query):
#     user_id = callback_query.from_user.id
#
#     # Установить таймер
#     if callback_query.data in ["5", "10", "15", "20", "30", "60", "90", "120", "180"]:
#         time_minutes = int(callback_query.data)
#         time_seconds = time_minutes * 60
#         subprocess.run(["shutdown", "/s", "/t", str(time_seconds), "/d", "p:0:0"])
#         await callback_query.message.reply(f"Таймер на выключение компьютера установлен на {time_minutes} минут.")
#
#     # Задать время таймера
#     elif callback_query.data == "set_time":
#         user_states[user_id] = {"set_time": True}
#         await callback_query.message.reply("Введите количество минут:")
#
#     # Отмена таймера
#     elif callback_query.data == "cancel":
#         subprocess.run(["shutdown", "/a"])
#         if user_states.get(user_id):
#             del user_states[user_id]
#         await callback_query.message.reply("Таймер отменен.")
#
#     # Управление плеером
#     elif callback_query.data in ["timeline_back_ten", "timeline_forward_ten", "timeline_back_once", "timeline_forward_once",
#                                  "vol_plus", "vol_minus", "vol_max", "vol_min", "play_n_pause", 'blank']:
#         funcs.player_control_commands(callback_query)
#
#     else:
#         # Регулировка громкости
#         percent_change = int(callback_query.data)
#         funcs.adjust_volume(percent_change)
#         await callback_query.answer()
#
# # Устанавливаем список команд бота
# bot_commands = [
#     BotCommand(command='shutdown', description='Выключить компьютер'),
#     BotCommand(command='restart', description='Перезагрузить компьютер'),
#     BotCommand(command='timer', description='Установить таймер на выключение компьютера'),
#     BotCommand(command='volume', description='Регулировка громкости'),
#     BotCommand(command='player_control', description='Управление плеером')
# ]
#
# #Запускаем клиент
# client.start()
#
# #Устанавливаем список команд бота
# client.set_bot_commands(bot_commands)
#
# #Входим в режим прослушивания сообщений
# idle()