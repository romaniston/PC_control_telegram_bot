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


def execute_anydesk(anydesk_path, message):
    try:
        subprocess.Popen([anydesk_path], start_new_session=True)
        print("INFO: AnyDesk is started")
        result = message.answer('Отправлена команда запуска "AnyDesk"')
        return result
    except FileNotFoundError:
        print('ERROR: "AnyDesk.exe" is not found on this path')
        result = message.answer('Отправлена команда запуска "AnyDesk"')
        return result
    except Exception as exc:
        print(f"ERROR: {exc}")
        result = message.answer('Отправлена команда запуска "AnyDesk"')
        return result


