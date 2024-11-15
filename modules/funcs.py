import subprocess
import pyautogui
from time import time


def give_tg_id(message):
    return message.from_user.id





# Функция для проверки пароля
def check_password(input_password, password):
    return input_password == password

# Таймаут свободного доступа без пароля на 120 минут после успешного ввода
def password_valid(tg_id, last_password_time):
    return tg_id in last_password_time and time() - last_password_time[tg_id] < 7200

# Функция для регулировки громкости с помощью тула NirCMD
def adjust_volume(volume_change):
    try:
        #Вызов NirCMD
        subprocess.run(["nircmd.exe", "setsysvolume", str(volume_change)])
    except FileNotFoundError:
        print("Произошла ошибка. Проверьте наличие NirCMD.exe в диркетории с программой")


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