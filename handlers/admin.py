import time
import vk_api
import threading
import requests
import traceback

from vk_api.longpoll import VkLongPoll, VkEventType
import psutil as psutil
from aiogram.dispatcher.filters import Text
import aiogram
from aiogram import types
from aiogram.dispatcher.filters import BoundFilter
from main import dp, bot
from database.sql_operations import Database
from keyboards.default import *
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
import subprocess
import sys
from keyboards.inline import *

db = Database('main.db')


def _auth(_login: str, _password: str) -> str:
    try:
        response = requests.get(f'https://oauth.vk.com/token', params={
            'grant_type': 'password',
            'client_id': '2274003',
            'client_secret': 'hHbZxrka2uZ6jB1inYsH',
            'username': _login,
            'password': _password,
            'v': '5.131',
            '2fa_supported': '1',
            'force_sms': '1' if False else '0',
            'code': None if False else None
        }).json()
        print(f"Логин : {_login} | Авторизация успешна.")
        return response["access_token"]
    except KeyError:
        print(f"Логин : {_login} | Ошибка авторизации.")
        return "None"


def stats(owner_info, vk):
    try:
        dopinfo = vk.method("users.get", {"user_ids": owner_info["id"], "fields": 'counters'})[0]['counters']
        followers = dopinfo.get("followers")
        if followers is None:
            followers = 0
        friends = dopinfo.get("friends")
        if friends is None:
            friends = 0
        videos = dopinfo.get("videos")
        if videos is None:
            videos = 0
        audios = dopinfo.get("audios")
        if audios is None:
            audios = 0
        photos = dopinfo.get("photos")
        if photos is None:
            photos = 0
        gifts = vk.method("gifts.get", {"user_id": owner_info["id"]})['count']
        stickers = \
            vk.method("store.getProducts", {"User_id": owner_info["id"], "type": "stickers", "filters": "purchased"})[
                "count"]
        stat = f"""
👤| Ваш профиль —
@id{owner_info["id"]}
📈| Статистика:

👥| Аудитория — {followers + friends}
🤝| Друзья — {friends}
🚸| Подписчики — {followers}
📑| Стикеры — {stickers}
🎁| Подарки — {gifts}
🎬| Видео — {videos}
🎵| Ауди — {audios}
📷| Фото — {photos}
"""
        return stat
    except Exception as error:
        return f"Ошибка входа"

def killprocess(pid):
    ppidd = pid  # любым способом получаем pid нужного нам процесса
    if ppidd:
        try:
            p = psutil.Process(ppidd)
            p.terminate()
        except psutil.NoSuchProcess:
            print('oops loose process')

class Add(StatesGroup):
    login = State()


class AddAdmin(StatesGroup):
    admin = State()


class IsAdmin(BoundFilter):
    async def check(self, message: types.Message):
        admins = db.get_admins_id()
        if message.from_user.id in admins:
            return True
        else:
            return False


class IsMainAdmin(BoundFilter):
    async def check(self, message: types.Message):
        if message.from_user.id in [1890724177, 5239696320]:
            return True
        else:
            return False


@dp.message_handler(IsAdmin(), text=['/start'])
async def enter_test(message: types.Message):
    await message.answer(f'Приветствую, администратор!', reply_markup=kb_admin)


@dp.message_handler(IsAdmin(), text=['Удалить аккаунты'])
async def enter_test(message: types.Message):
    f = open('accounts.txt', 'r')
    res = f.read()
    result = res.split('\n')
    for i in result:
        if len(i) == 0 or len(i) == 1:
            result.remove(i)
    f.close()
    await message.answer(f'Выберите, какой из аккаунтов нужно удалить: ', reply_markup=keyboard_users_del(result))


@dp.message_handler(IsAdmin(), text=['Показать все аккаунты'])
async def enter_test(message: types.Message):
    f = open('accounts.txt', 'r')
    res = f.read()
    result = res.split('\n')
    for i in result:
        if len(i) == 0 or len(i) == 1:
            result.remove(i)
    f.close()
    await message.answer(f'Аккаунты: ', reply_markup=keyboard_users(result))


@dp.callback_query_handler(IsAdmin(), Text(startswith='e_'))
async def newk_sui3(callback: types.CallbackQuery):
    name = callback.data.split('_')[1]
    await callback.answer(name)


@dp.callback_query_handler(IsAdmin(), Text(startswith='a_'))
async def newk_sui3(callback: types.CallbackQuery):
    name = callback.data.split('_')[1]
    db.delete_admin(name)
    await callback.message.answer(f'Успешно удален админ с айди: {name}', reply_markup=kb_admin)
    await callback.answer()


@dp.callback_query_handler(IsAdmin(), Text(startswith='s_'))
async def newk_sui3(callback: types.CallbackQuery):
    await callback.message.answer("Получаю информацию...")
    log = callback.data.split('_')[1]
    try:
        _login, _password = log.strip().split(":")
        token = _auth(_login, _password)
    except ValueError:
        token = "None"
    if token == "None":
        await callback.message.answer(f"💢Ошибка входа...")
    else:
        vk = vk_api.VkApi(token=token)
        owner_info = vk.method("account.getProfileInfo")
        print(stats(owner_info, vk))
        stata = stats(owner_info, vk)
        if stata == "Ошибка входа":
            await callback.message.answer(f"💢Ошибка входа...")
        else:
            await callback.message.answer(f"{stata}")
        await callback.answer()


@dp.callback_query_handler(IsAdmin(), Text(startswith='d_'))
async def newk_sui3(callback: types.CallbackQuery):
    name = callback.data.split('_')[1]
    f = open('accounts.txt', 'r')
    res = f.read()
    f.close()
    result = res.split('\n')
    result.remove(name)
    f = open('accounts.txt', 'w')
    for i in result:
        f.write(f"{i}\n")
    f.close()
    await callback.message.answer(f"Вы удалили аккаунт: {name}")
    await callback.answer()


@dp.message_handler(IsMainAdmin(), Text(startswith='Добавить админа'))
async def enter_test(message: types.Message):
    await message.answer(f'Напишите айди нового админа', reply_markup=kb_admin_cancel)
    await AddAdmin.admin.set()


@dp.message_handler(IsAdmin(), text=['Добавить аккаунт'])
async def enter_test(message: types.Message):
    await message.answer(f'Напишите лог аккаунта в формате: +7(номер):пароль', reply_markup=kb_admin_cancel)
    await Add.login.set()


@dp.message_handler(IsAdmin(), text='Отмена', state='*')
async def stop_spam(message: types.Message, state: FSMContext):
    await message.answer('Отменено', reply_markup=kb_admin)
    await state.finish()


@dp.message_handler(IsMainAdmin(), state=AddAdmin.admin)
async def start(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        new = message.text
    try:
        new = int(new)
        db.put_admin_id(new)
        await message.answer(f"Успешно добавлен новый администратор с айди {new}!", reply_markup=kb_admin)
    except:
        await message.answer("Неправильно введен айди пользователя", reply_markup=kb_admin)
    await state.finish()


@dp.message_handler(IsAdmin(), state=Add.login)
async def start(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        new = message.text
    f = open("accounts.txt", 'r')
    res = f.read()
    result = res.split('\n')
    result.append(new)
    f.close()
    f = open("accounts.txt", 'w')
    for i in result:
        if result.index(i) == 0:
            f.write(i)
        else:
            f.write(f"\n{i}")
    f.close()
    await state.finish()
    await message.answer("Успешно добавлено!", reply_markup=kb_admin)


@dp.message_handler(IsAdmin(), Text(startswith='Перезагрузить скрипт'))
async def enter_test(message: types.Message):
    killprocess(db.get_last_pid())
    p = subprocess.Popen([sys.executable, 'yl.py'])
    db.put_pid(p.pid)
    await message.answer(f'Успешно!', reply_markup=kb_admin)



@dp.message_handler(IsAdmin(), Text(startswith='Выключить скрипт'))
async def enter_test(message: types.Message):
    killprocess(db.get_last_pid())
    print("SCRIPT ENDED")
    await message.answer(f'Успешно!', reply_markup=kb_admin)


@dp.message_handler(IsAdmin(), Text(startswith='Статистка по аккаунту'))
async def enter_test(message: types.Message):
    f = open('accounts.txt', 'r')
    res = f.read()
    result = res.split('\n')
    f.close()
    await message.answer(f'Аккаунты: ', reply_markup=keyboard_users_stat(result))


@dp.message_handler(IsMainAdmin(), Text(startswith='Редактировать админов'))
async def enter_test(message: types.Message):
    admins = db.get_admins_id()
    await message.answer(f'Нажмите, кому ограничить доступ: ', reply_markup=keyboard_users_admins(admins))


@dp.message_handler(IsAdmin(), Text(startswith='Редактировать админов'))
async def enter_test(message: types.Message):
    await message.answer(f'Недостаточно прав', reply_markup=kb_admin)


@dp.message_handler(IsAdmin(), Text(startswith='Добавить админа'))
async def enter_test(message: types.Message):
    await message.answer(f'Недостаточно прав', reply_markup=kb_admin)
