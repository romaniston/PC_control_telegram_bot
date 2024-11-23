import subprocess
import pyautogui
import psutil
from time import time


def give_tg_id(message):
    return message.from_user.id


def check_password(input_password, password):
    return input_password == password


def input_key_in_dict(tg_id, last_time_password):
    try:
        key_exist_check = last_time_password.get(tg_id)
    except KeyError:
        last_time_password[tg_id] = None


# access granted after correct password in n seconds
access_time_val = 3
def access_granted(tg_id, last_time_password):
    last_time_password_var = last_time_password.get(tg_id)

    if last_time_password_var == None:
        return False
    elif last_time_password_var != None:
        current_time = time()
        access_time = current_time - last_time_password_var
        if access_time > access_time_val:
            return False
        elif access_time < access_time_val:
            return True


def adjust_volume(volume_val):
        subprocess.run(['nircmd.exe', 'setsysvolume', str(volume_val)])


def many_press_func(button, repite):
    for it in range(repite):
        pyautogui.press(button)


def is_process_running(process_name, need_to_shutdown):
    processes = []
    for proc in psutil.process_iter(['name']):
        if proc.info['name'] == process_name:
            if not need_to_shutdown:
                return True
            elif need_to_shutdown:
                processes.append(proc)
    if not need_to_shutdown:
        return False
    if need_to_shutdown:
        return processes


def execute_anydesk(anydesk_path):
    try:
        anydesk_processes = is_process_running('AnyDesk.exe', need_to_shutdown=False)
        if not anydesk_processes:
            subprocess.Popen([anydesk_path], start_new_session=True)
            print("INFO: AnyDesk is started")
            return 'Отправлена команда запуска AnyDesk'
        elif anydesk_processes:
            print("INFO: AnyDesk is already running.")
            return 'AnyDesk уже запущен'
    except FileNotFoundError:
        print('ERROR: "AnyDesk.exe" is not found on this path')
        return 'AnyDesk не найден по заданному пути (см. "Config.ini")'
    except Exception as exc:
        print(f"ERROR: {exc}")
        return 'Возникла ошибка (см. консоль)'


def shutdown_anydesk():
    try:
        anydesk_processes = is_process_running('AnyDesk.exe', need_to_shutdown=True)
        if anydesk_processes:
            for proc in anydesk_processes:  # Terminate all anydesk processes
                proc.terminate()
                proc.wait()
            print("INFO: AnyDesk is shutdown")
            return 'Отправлена команда выключения AnyDesk'
        elif not anydesk_processes:
            print("INFO: AnyDesk is not executed")
            return 'В данный момент AnyDesk не запущен'
    except Exception as exc:
        print(f"ERROR: {exc}")
        return 'Возникла ошибка (см. консоль)'
