from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def keyboard_users(res):
    the_keyboard = InlineKeyboardMarkup()
    for i in res:
        the_keyboard.add(InlineKeyboardButton(text=i, callback_data=f"e_{i}"))
    return the_keyboard


def keyboard_users_del(res):
    the_keyboard = InlineKeyboardMarkup()
    for i in res:
        the_keyboard.add(InlineKeyboardButton(text=i, callback_data=f"d_{i}"))
    return the_keyboard


def keyboard_users_stat(res):
    the_keyboard = InlineKeyboardMarkup()
    for i in res:
        the_keyboard.add(InlineKeyboardButton(text=i, callback_data=f"s_{i}"))
    return the_keyboard


def keyboard_users_admins(admins):
    the_keyboard = InlineKeyboardMarkup()
    for i in admins:
        the_keyboard.add(InlineKeyboardButton(text=i, callback_data=f"a_{i}"))
    return the_keyboard
