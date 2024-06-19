import subprocess
import pyautogui
from time import time
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

# Функция для проверки пароля
def check_password(message, PASSWORD):
    return message.text.strip() == PASSWORD

# Таймаут свободного доступа без пароля на 120 минут после успешного ввода
def password_valid(user_id, last_password_time):
    return user_id in last_password_time and time() - last_password_time[user_id] < 7200

# Функция для регулировки громкости с помощью тула NirCMD
def adjust_volume(volume_change):
    try:
        #Вызов NirCMD
        subprocess.run(["nircmd.exe", "setsysvolume", str(volume_change)])
    except FileNotFoundError:
        print("Произошла ошибка. Проверьте наличие NirCMD.exe в диркетории с программой")

# Клавиатуры для вывода юзаку
def inline_keyboards_template(command):
    if command == 'timer':
        reply_markup = InlineKeyboardMarkup(
            [
                [InlineKeyboardButton("5 минут", callback_data="5"),
                 InlineKeyboardButton("10 минут", callback_data="10"),
                 InlineKeyboardButton("15 минут", callback_data="15")],
                [InlineKeyboardButton("20 минут", callback_data="20"),
                 InlineKeyboardButton("30 минут", callback_data="30"),
                 InlineKeyboardButton("60 минут", callback_data="60")],
                [InlineKeyboardButton("90 минут", callback_data="90"),
                 InlineKeyboardButton("120 минут", callback_data="120"),
                 InlineKeyboardButton("180 минут", callback_data="180")],
                [InlineKeyboardButton("Задать время", callback_data="set_time")],
                [InlineKeyboardButton("Отмена", callback_data="cancel")],
            ]
        )

    elif command == 'volume':
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
                [InlineKeyboardButton("100%", callback_data="65535")]
            ]
        )

    elif command == 'player_control':
        reply_markup = InlineKeyboardMarkup(
            [
                [InlineKeyboardButton(" ", callback_data="blank")],
                [InlineKeyboardButton("<<< once", callback_data="timeline_back_once"),
                 InlineKeyboardButton("once >>>", callback_data="timeline_forward_once")],
                [InlineKeyboardButton(" ", callback_data="blank")],
                [InlineKeyboardButton("<<< 10", callback_data="timeline_back_ten"),
                 InlineKeyboardButton("10 >>>", callback_data="timeline_forward_ten")],
                [InlineKeyboardButton(" ", callback_data="blank")],
                [InlineKeyboardButton("Pause / Play", callback_data="play_n_pause")],
                [InlineKeyboardButton(" ", callback_data="blank")],
                [InlineKeyboardButton("Volume +", callback_data="vol_plus")],
                [InlineKeyboardButton("Volume -", callback_data="vol_minus")],
                [InlineKeyboardButton(" ", callback_data="blank")],
                [InlineKeyboardButton("Volume MAX", callback_data="vol_max")],
                [InlineKeyboardButton("Volume MIN", callback_data="vol_min")],
                [InlineKeyboardButton(" ", callback_data="blank")],
            ]
        )
    return reply_markup

# Итератор для управления плеером (длительные перемотки и volume min, max)
def many_press_func(button, repit):
    for temp in range(repit):
        pyautogui.press(button)

# Обработки нажатий на кнопки управления плеером
def player_control_commands(callback_query,):
    if callback_query.data == 'timeline_back_once':
        return pyautogui.press('left')
    elif callback_query.data == 'timeline_forward_once':
        return pyautogui.press('right')
    elif callback_query.data == 'timeline_back_ten':
        return many_press_func('left', 10)
    elif callback_query.data == 'timeline_forward_ten':
        return many_press_func('right', 10)
    elif callback_query.data == 'vol_minus':
        return pyautogui.press('down')
    elif callback_query.data == 'vol_plus':
        return pyautogui.press('up')
    elif callback_query.data == 'vol_min':
        return many_press_func('down', 20)
    elif callback_query.data == 'vol_max':
        return many_press_func('up', 20)
    elif callback_query.data == 'play_n_pause':
        return pyautogui.press('space')
    elif callback_query.data == 'blank':
        pass