from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram import types

kb_admin = types.ReplyKeyboardMarkup(resize_keyboard=True)
kb_admin.row(KeyboardButton(text='Добавить аккаунт'), KeyboardButton(text='Статистка по аккаунту'))
kb_admin.row(KeyboardButton(text='Удалить аккаунты'), KeyboardButton(text='Показать все аккаунты'))
kb_admin.add(KeyboardButton(text='Перезагрузить скрипт'), KeyboardButton(text='Выключить скрипт'))
kb_admin.row(KeyboardButton(text='Добавить админа'), KeyboardButton(text='Редактировать админов'))

kb_admin_cancel = types.ReplyKeyboardMarkup(resize_keyboard=True)
kb_admin_cancel.add(KeyboardButton(text='Отмена'))
gender = ReplyKeyboardMarkup(
    [
        [
            KeyboardButton(text=f'Мужской')
        ],
        [
            KeyboardButton(text=f'Женский')
        ],
    ], one_time_keyboard=True, resize_keyboard=True)
