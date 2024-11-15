from aiogram.types import BotCommand
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


def setup_bot_commands():
    bot_commands = [
        BotCommand(command="/shutdown", description="Выключить ПК"),
        BotCommand(command="/reboot", description="Перезагрузить ПК"),
        BotCommand(command="/timer", description="Установить таймер на выключение"),
        BotCommand(command="/volume", description="Регулировка громкости"),
        BotCommand(command="/player", description="Управление плеером"),
        BotCommand(command="/anydesk_on", description="Запуск AnyDesk"),
        BotCommand(command="/anydesk_off", description="Выключение AnyDesk")
    ]
    return bot_commands


def keyboard_timer():
    reply_markup = InlineKeyboardMarkup(
        inline_keyboard=
        [
            [InlineKeyboardButton(text="5 минут", callback_data="timer_5"),
             InlineKeyboardButton(text="10 минут", callback_data="timer_10"),
             InlineKeyboardButton(text="15 минут", callback_data="timer_15")],
            [InlineKeyboardButton(text="20 минут", callback_data="timer_20"),
             InlineKeyboardButton(text="30 минут", callback_data="timer_30"),
             InlineKeyboardButton(text="60 минут", callback_data="timer_60")],
            [InlineKeyboardButton(text="90 минут", callback_data="timer_90"),
             InlineKeyboardButton(text="120 минут", callback_data="timer_120"),
             InlineKeyboardButton(text="180 минут", callback_data="timer_180")],
            [InlineKeyboardButton(text="Задать время", callback_data="set_time")],
            [InlineKeyboardButton(text="Отменить таймер", callback_data="cancel_timer")],
        ]
    )
    return reply_markup


def keyboard_volume():
    reply_markup = InlineKeyboardMarkup(
        inline_keyboard=
        [
            [InlineKeyboardButton(text="0%", callback_data="vol_0")],
            [InlineKeyboardButton(text="5%", callback_data="vol_3276")],
            [InlineKeyboardButton(text="10%", callback_data="vol_6553")],
            [InlineKeyboardButton(text="20%", callback_data="vol_13106")],
            [InlineKeyboardButton(text="30%", callback_data="vol_19659")],
            [InlineKeyboardButton(text="40%", callback_data="vol_26212")],
            [InlineKeyboardButton(text="50%", callback_data="vol_32765")],
            [InlineKeyboardButton(text="60%", callback_data="vol_39318")],
            [InlineKeyboardButton(text="70%", callback_data="vol_45871")],
            [InlineKeyboardButton(text="80%", callback_data="vol_52424")],
            [InlineKeyboardButton(text="90%", callback_data="vol_58977")],
            [InlineKeyboardButton(text="100%", callback_data="vol_65535")]
        ]
    )
    return reply_markup


def keyboard_player_control():
    reply_markup = InlineKeyboardMarkup(
        inline_keyboard=
        [
            [InlineKeyboardButton(text=" ", callback_data="blank")],
            [InlineKeyboardButton(text="<<< 10 times", callback_data="timeline_back_10"),
             InlineKeyboardButton(text="10 times >>>", callback_data="timeline_forward_10")],
            [InlineKeyboardButton(text=" ", callback_data="blank")],
            [InlineKeyboardButton(text="<<< once", callback_data="timeline_back_once"),
             InlineKeyboardButton(text="once >>>", callback_data="timeline_forward_once")],
            [InlineKeyboardButton(text=" ", callback_data="blank")],
            [InlineKeyboardButton(text="Pause / Play", callback_data="play_n_pause")],
            [InlineKeyboardButton(text=" ", callback_data="blank")],
            [InlineKeyboardButton(text="Volume -", callback_data="vol_minus"),
            InlineKeyboardButton(text="Volume +", callback_data="vol_plus")],
            [InlineKeyboardButton(text=" ", callback_data="blank")],
            [InlineKeyboardButton(text="Volume MIN", callback_data="vol_min"),
            InlineKeyboardButton(text="Volume MAX", callback_data="vol_max")],
            [InlineKeyboardButton(text=" ", callback_data="blank")],
        ]
    )
    return reply_markup