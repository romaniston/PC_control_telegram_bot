import subprocess
import configparser
import pyautogui
from modules import keyboards, funcs
from aiogram.types import Message, CallbackQuery
from aiogram import F, Router
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
from aiogram.filters import Command, CommandStart
from time import time


router_handlers = Router()

config = configparser.ConfigParser()
config.read('config.ini')
password = config['Telegram']['PASSWORD']
anydesk_path = config['Anydesk']['path']

last_time_password = {}

list_timer_data = ['timer_5', 'timer_10', 'timer_15', 'timer_20', 'timer_30', 'timer_60', 'timer_90', 'timer_120',
                   'timer_180', 'set_time', 'cancel_timer']

list_volume_data = ['vol_0', 'vol_3276', 'vol_6553', 'vol_13106', 'vol_19659', 'vol_26212', 'vol_32765', 'vol_39318',
                    'vol_45871', 'vol_52424', 'vol_58977', 'vol_65535']

list_player_data = ['timeline_back_once', 'timeline_forward_once', 'timeline_back_10', 'timeline_forward_10',
                    'vol_minus', 'vol_plus', 'vol_min', 'vol_max', 'play_n_pause', 'blank']


class Commands(StatesGroup):
    shutdown = State()
    reboot = State()
    timer = State()
    timer_set_time = State()
    volume = State()
    player = State()
    anydesk = State()


@router_handlers.message(CommandStart())
async def start_bot(message: Message):
    await message.answer('Hello World :3')


@router_handlers.message(Command('shutdown'))
async def shutdown_computer_pass(message: Message, state: FSMContext):
    tg_id = funcs.give_tg_id(message)

    await state.clear()
    await state.update_data(tg_id=tg_id)

    funcs.input_key_in_dict(tg_id, last_time_password)

    if funcs.access_granted(tg_id, last_time_password):
        # subprocess.run(["shutdown", "/s", "/t", "1"])
        await message.answer("Компьютер будет выключен.")
        await state.clear()
    else:
        await state.set_state(Commands.shutdown)
        await message.answer("Введите пароль для выполнения команды:")


@router_handlers.message(Commands.shutdown)
async def shutdown_computer(message: Message, state: FSMContext):
    global password
    input_password = message.text
    fsm_data = await state.get_data()
    tg_id = fsm_data.get('tg_id')

    if funcs.check_password(input_password, password):
        # subprocess.run(["shutdown", "/s", "/t", "1"])
        await message.answer("Компьютер будет выключен.")
        await state.clear()
        last_time_password[tg_id] = time()
    else:
        await message.answer("Неверный пароль")
        await state.clear()


@router_handlers.message(Command('reboot'))
async def reboot_computer_pass(message: Message, state: FSMContext):
    tg_id = funcs.give_tg_id(message)

    await state.clear()
    await state.update_data(tg_id=tg_id)

    funcs.input_key_in_dict(tg_id, last_time_password)

    if funcs.access_granted(tg_id, last_time_password):
        # subprocess.run(["shutdown", "/r", "/t", "1"])
        await message.answer("Компьютер будет перезагружен.")
        await state.clear()
    else:
        await state.set_state(Commands.reboot)
        await message.answer("Введите пароль для выполнения команды:")


@router_handlers.message(Commands.reboot)
async def reboot_computer(message: Message, state: FSMContext):
    global password
    input_password = message.text
    fsm_data = await state.get_data()
    tg_id = fsm_data.get('tg_id')

    if funcs.check_password(input_password, password):
        # subprocess.run(["shutdown", "/r", "/t", "1"])
        await message.answer("Компьютер будет перезагружен.")
        await state.clear()
        last_time_password[tg_id] = time()
    else:
        await message.answer("Неверный пароль")
        await state.clear()


@router_handlers.message(Command('timer'))
async def timer_pass(message: Message, state: FSMContext):
    global password
    tg_id = funcs.give_tg_id(message)

    await state.clear()
    await state.update_data(tg_id=tg_id)

    funcs.input_key_in_dict(tg_id, last_time_password)

    if funcs.access_granted(tg_id, last_time_password):
        reply_markup = keyboards.keyboard_timer()
        await message.answer("Выберите время для выключения компьютера:", reply_markup=reply_markup)
    else:
        await state.set_state(Commands.timer)
        await message.answer("Введите пароль для выполнения команды:")


@router_handlers.message(Commands.timer)
async def timer(message: Message, state: FSMContext):
    global password
    input_password = message.text
    fsm_data = await state.get_data()
    tg_id = fsm_data.get('tg_id')

    if funcs.check_password(input_password, password):
        reply_markup = keyboards.keyboard_timer()
        await message.answer("Выберите время для выключения компьютера:", reply_markup=reply_markup)
        last_time_password[tg_id] = time()
    else:
        await message.answer("Неверный пароль")
        await state.clear()


@router_handlers.callback_query(lambda callback: callback.data in list_timer_data)
async def timer_action(callback: CallbackQuery, state: FSMContext):
    message = callback.data
    data = message.split('_')
    data_first_var = str(data[0])
    minutes = str(data[1])

    if data_first_var == 'timer':
        time_minutes = int(minutes)
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


@router_handlers.message(Commands.timer_set_time)
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


@router_handlers.message(Command('volume'))
async def volume_pass(message: Message, state: FSMContext):
    global password
    tg_id = funcs.give_tg_id(message)

    await state.clear()
    await state.update_data(tg_id=tg_id)

    funcs.input_key_in_dict(tg_id, last_time_password)

    if funcs.access_granted(tg_id, last_time_password):
        reply_markup = keyboards.keyboard_volume()
        await message.answer("Регулировка громкости:", reply_markup=reply_markup)
        await state.clear()
    else:
        await state.set_state(Commands.volume)
        await message.answer("Введите пароль для выполнения команды:")


@router_handlers.message(Commands.volume)
async def volume(message: Message, state: FSMContext):
    global password
    input_password = message.text
    fsm_data = await state.get_data()
    tg_id = fsm_data.get('tg_id')

    if funcs.check_password(input_password, password):
        reply_markup = keyboards.keyboard_volume()
        await message.answer("Регулировка громкости:", reply_markup=reply_markup)
        last_time_password[tg_id] = time()
    else:
        await message.answer("Неверный пароль")

    await state.clear()


@router_handlers.callback_query(lambda callback: callback.data in list_volume_data)
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
        await callback.answer('')  # fix of long lighting inline button


@router_handlers.message(Command('player'))
async def player_pass(message: Message, state: FSMContext):
    global password
    tg_id = funcs.give_tg_id(message)

    await state.clear()
    await state.update_data(tg_id=tg_id)

    funcs.input_key_in_dict(tg_id, last_time_password)

    if funcs.access_granted(tg_id, last_time_password):
        reply_markup = keyboards.keyboard_player_control()
        await message.answer("Управление плеером", reply_markup=reply_markup)
        await state.clear()
    else:
        await state.set_state(Commands.player)
        await message.answer("Введите пароль для выполнения команды:")


@router_handlers.message(Commands.player)
async def player(message: Message, state: FSMContext):
    global password
    input_password = message.text
    fsm_data = await state.get_data()
    tg_id = fsm_data.get('tg_id')

    if funcs.check_password(input_password, password):
        reply_markup = keyboards.keyboard_player_control()
        await message.answer("Управление плеером", reply_markup=reply_markup)
        last_time_password[tg_id] = time()
    else:
        await message.answer("Неверный пароль")

    await state.clear()


@router_handlers.callback_query(lambda callback: callback.data in list_player_data)
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


@router_handlers.message(Command('anydesk'))
async def anydesk_ctrl_pass(message: Message, state: FSMContext):
    global password
    tg_id = funcs.give_tg_id(message)

    await state.clear()
    await state.update_data(tg_id=tg_id)

    funcs.input_key_in_dict(tg_id, last_time_password)

    if funcs.access_granted(tg_id, last_time_password):
        await message.answer('Управление AnyDesk', reply_markup=keyboards.keyboard_anydesk())
    else:
        await state.set_state(Commands.anydesk)
        await message.answer("Введите пароль для выполнения команды:")


@router_handlers.message(Commands.anydesk)
async def anydesk_ctrl(message: Message, state: FSMContext):
    global password
    input_password = message.text
    fsm_data = await state.get_data()
    tg_id = fsm_data.get('tg_id')

    if funcs.check_password(input_password, password):
        await message.answer('Управление AnyDesk', reply_markup=keyboards.keyboard_anydesk())
        last_time_password[tg_id] = time()
    else:
        await message.answer("Неверный пароль")

    await state.clear()


@router_handlers.callback_query(F.data == '_adesk_will_be_on')
async def anydesk_on(callback: CallbackQuery):
    info_mes = funcs.execute_anydesk(anydesk_path)
    await callback.message.edit_text(info_mes)


@router_handlers.callback_query(F.data == '_adesk_will_be_off')
async def anydesk_off(callback: CallbackQuery):
    info_mes = funcs.shutdown_anydesk()
    await callback.message.edit_text(info_mes)
    