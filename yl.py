import vk_api
import threading
import requests
import traceback
import time

from vk_api.longpoll import VkLongPoll, VkEventType


def sender(vk, event, text):
    vk.method('messages.send', {'peer_id': event.peer_id, 'message': text, 'random_id': 0})


def edit_message(vk, event, msg="", atts=""):
    try:
        return True, vk.method("messages.edit",
                               {"peer_id": event.peer_id, "keep_forward_messages": 1, "message": "{}".format(msg),
                                "attachment": atts, "message_id": event.message_id, "random_id": 0})
    except Exception as error:
        return False, error


def delets(vk, event):
    sender(vk, event, "Удаляю,чекай консоль")
    owner_info = vk.method("account.getProfileInfo")
    try:
        kol = event.text.split('\n')[1]
    except IndexError:
        edit_message(vk, event, 'Число нужно указать с новой строки')
    get = vk.method('friends.get', {'user_id': owner_info['id'], 'count': kol})['items']
    for i in get:
        # time.sleep(10)
        a = vk.method('friends.delete', {'user_id': i})
        print(f'user deleted: @id{i}')


def join(_login: str, token):
    vk = vk_api.VkApi(token=token)
    lp = VkLongPoll(vk)
    try:
        vk.method('messages.joinChatByInviteLink', {'link': 'https://vk.me/join/sOsId6qbwdu/sZ3YunlS682GWGsC0oilB5E='})
        return print(f"Логин : {_login} | Успешно инвайтнулся.")
    except Exception as e:
        return print(f"Логин : {_login} | Error | {e}")


def lp_set(token):
    try:
        vk = vk_api.VkApi(token=token)
        lp = VkLongPoll(vk)
    except Exception as error:
        if str(error) in cfg.NO_SEND_ERROR:
            print(
                f"""{owner_info["first_name"]} {owner_info["last_name"]} @id{str(owner_info["id"])} | Line: {traceback.format_exc().partition('line ')[2].partition(', in')[0]} | {error}""")

            return False, None
        else:
            logger.error(
                f"""{owner_info["first_name"]} {owner_info["last_name"]} @id{str(owner_info["id"])} | Line: {traceback.format_exc().partition('line ')[2].partition(', in')[0]} | {error}""")
            return False, None
    else:
        return lp, vk


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
        return f"💢 Произошла ошибка./n💬 Информация об ошибке:/n{error}"


def scripts(owner_info, token):
    time_onl_start = time_onl_present = time_req_start = time_req_present = time_undr_start = time_undr_present = time_frie_start = time_frie_present = 0
    try:
        vkme = vk_api.VkApi(token=token)
        vkme._auth_token()
    except Exception as error:
        print(f"Ошибка подключения скриптов. {error}")
    else:
        while True:
            condition_on = "on"
            condition_ar = "on"
            condition_ot = "on"
            condition_dr = "on"
            try:
                if condition_on == "on":
                    try:
                        if (time_onl_start + time_onl_present) < int(str(time.time()).split(".", maxsplit=1)[0]):
                            time_onl_start = int(str(time.time()).split(".", maxsplit=1)[0])
                            time_onl_present = 250
                            vkme.method("account.setOnline")
                            print(
                                f"""@id{str(owner_info["id"])} | USER | AutoONL | Set online user @id{owner_info["id"]}""")
                    except Exception as error:
                        time_onl_start = int(str(time.time()).split(".", maxsplit=1)[0])
                        time_onl_present = 250
                        print(
                            f"""@id{str(owner_info["id"])} | USER | AutoONL | {error} | Line: {traceback.format_exc().partition('line ')[2].partition(', in')[0]}""")

                if condition_ar == "on":
                    if (time_req_start + time_req_present) < int(str(time.time()).split(".", maxsplit=1)[0]):
                        try:
                            responce, user_list = vkme.method("friends.getRecommendations",
                                                              {"filter": "mutual",
                                                               "fields": "common_count, is_friend, blacklisted_by_me, online"})[
                                                      "items"], []
                            for user in responce:
                                if user["is_friend"] == 0 and user["blacklisted_by_me"] == 0 and user["online"] == 1:
                                    user_list.append([user["common_count"], user["id"]])
                            user_list.sort()
                            if len(user_list) > 15:
                                vol = 0
                                for i in user_list[-15:]:
                                    if vkme.method("friends.add", {"user_id": i[1]}) == 1:
                                        vol += 5
                                        print(
                                            f"""@id{str(owner_info["id"])} | USER | AutoREC | Invite user @id{i[1]}""")
                                        time.sleep(3)
                                time_req_start = int(str(time.time()).split(".", maxsplit=1)[0])
                                time_req_present = 120
                            else:
                                time_req_start = int(str(time.time()).split(".", maxsplit=1)[0])
                                time_req_present = 120
                        except Exception as error:
                            time_req_start = int(str(time.time()).split(".", maxsplit=1)[0])
                            time_req_present = 120
                            print(
                                f"""@id{str(owner_info["id"])} | USER | AutoREC | {error} | Line: {traceback.format_exc().partition('line ')[2].partition(', in')[0]}""")

                if condition_ot == "on" and condition_ar == "off":
                    if (time_undr_start + time_undr_present) < int(str(time.time()).split(".", maxsplit=1)[0]):
                        try:
                            followers = vkme.method("friends.getRequests", {"count": 1, "out": 1})
                            if followers["count"] > 0:
                                vkme.method("wall.unsubscribe", {"owner_id": followers["items"][0]})
                                time.sleep(1)
                                vkme.method("friends.delete", {"user_id": followers["items"][0]})
                                time_undr_start = int(str(time.time()).split(".", maxsplit=1)[0])
                                time_undr_present = 90
                                print(
                                    f"""@id{str(owner_info["id"])} | USER | AutoOTP | Unsubscribed user @id{followers["items"][0]}""")
                            else:
                                time_undr_start = int(str(time.time()).split(".", maxsplit=1)[0])
                                time_undr_present = 30
                        except Exception as error:
                            time_undr_start = int(str(time.time()).split(".", maxsplit=1)[0])
                            time_undr_present = 90
                            print(
                                f"""@id{str(owner_info["id"])} | USER | AutoOTP | {error} | Line: {traceback.format_exc().partition('line ')[2].partition(', in')[0]}""")

                if condition_dr == "on" and (time_frie_start + time_frie_present) < int(
                        str(time.time()).split(".", maxsplit=1)[0]):
                    try:
                        followers = vkme.method("friends.getRequests", {"count": 1})
                        if followers["count"] > 0:
                            inj = vkme.method("users.get", {"user_ids": followers["items"][0]})[0].get("deactivated")
                            if inj == None:
                                vkme.method("friends.add", {"user_id": followers["items"][0]})
                                time_frie_start = int(str(time.time()).split(".", maxsplit=1)[0])
                                time_frie_present = 30
                                print(
                                    f"""@id{str(owner_info["id"])} | USER | AutoFRI | Accept user @id{followers["items"][0]}""")
                            else:
                                try:
                                    vkme.method("account.ban", {"owner_id": followers["items"][0]})
                                    vkme.method("account.unban", {"owner_id": followers["items"][0]})
                                except:
                                    vkme.method("friends.delete", {"user_id": followers["items"][0]})
                        else:
                            time_frie_start = int(str(time.time()).split(".", maxsplit=1)[0])
                            time_frie_present = 90
                    except Exception as error:
                        time_frie_start = int(str(time.time()).split(".", maxsplit=1)[0])
                        time_frie_present = 90
                        print(
                            f"""@id{str(owner_info["id"])} | USER | AutoFRI | {error} | Line: {traceback.format_exc().partition('line ')[2].partition(', in')[0]}""")
            except:
                print("error scripts")
                time.sleep(600)


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


def user(owner_info, token):
    while True:
        lp, vk = lp_set(token)
        if not lp:
            print("Lp OFF")
            break
        else:
            try:
                for event in lp.listen():
                    if event.type == VkEventType.MESSAGE_NEW and event.__dict__.get("text"):
                        if event.text == "stata" and event.from_me:
                            edit_message(vk, event, 'please wait..')
                            edit_message(vk, event, stats(owner_info, vk))
                        if event.text == "delete" and event.from_me:
                            threading.Thread(target=delets, args=(event,)).start()
                    if event.type == VkEventType.MESSAGE_NEW and event.__dict__.get("text"):
                        if event.text == "stats" and event.__dict__.get("text"):
                            sender(vk, event, stats(owner_info, vk))
                        if event.text == "kol" and event.__dict__.get("text"):
                            owner_info = vk.method("account.getProfileInfo")
                            get = vk.method('friends.get', {'user_id': owner_info['id']})['count']
                            sender(vk, event, f'На странице {get} друзьяшек')

            except:
                print("Ошибка лонгпула.")


def start():
    data = []
    with open("accounts.txt", 'r') as file:
        while True:
            line = file.readline()
            if not line:
                break
            _login, _password = line.strip().split(":")
            token = _auth(_login, _password)
            if token != "None":
                data.append(token)
    file.close()
    for token in data:
        vk = vk_api.VkApi(token=token)
        owner_info = vk.method("account.getProfileInfo")
        threading.Thread(target=scripts, args=(owner_info, token)).start()
        threading.Thread(target=user, args=(owner_info, token)).start()
        threading.Thread(target=join, args=(_login, token)).start()


if __name__ == "__main__":
    start()
