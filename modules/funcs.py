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


def adjust_volume(volume_val):
        subprocess.run(['nircmd.exe', 'setsysvolume', str(volume_val)])


def many_press_func(button, repite):
    for it in range(repite):
        pyautogui.press(button)
