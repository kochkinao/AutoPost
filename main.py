from telethon import TelegramClient
from telethon.tl.types import PeerChat, PeerChannel
import os

import pytz
from time import sleep

from datetime import datetime, time, timedelta
import json

# API данные для подключения к аккаунту
api_id = 25649641
api_hash = "d251d50d7a38842fa4efca07e8ae100d"

# Время отправки сообщений
first_send_media = "12:50"
text_post = "12:55"
channel = "13:06"
contacts = "13:10"
second_send_media = "13:15"

# Чат отправки
# forum = PeerChannel(channel_id=1616500560)
# forum2 = PeerChannel(channel_id=1451579619)
forum = PeerChat(chat_id=4541363679)

# Ветки отправки
rep = 51159


# rep2 = 33349


# Функция для вычисления
def is_work_time(start_time: str, end_time: str):
    now = pytz.timezone('Europe/Moscow').localize(datetime.now()).time()
    start = time.fromisoformat(start_time)
    end = time.fromisoformat(end_time)
    return any([now <= end, now >= start]) if not start < end else (start <= now <= end)


# Функция для вычисления времени для сна бота (сколько бот будет ждать рассылки)
def waiting_to_wake_up(start_time, end_time):
    start = datetime.strptime(start_time, '%H:%M')
    end = datetime.strptime(end_time, '%H:%M')
    hours = datetime.strptime("00:00", "%H:%M")
    result = datetime.strftime(hours - (start - end), '%H:%M')
    asd = timedelta(hours=int(result[0] + result[1]), minutes=int(result[3] + result[4]))
    return round(asd.total_seconds())


# Подключение к аккаунту
with TelegramClient('andrey', api_id, api_hash, system_version='4.10.2') as client:
    async def send_media():
        # Получаем список файлов
        files = os.listdir("./media")
        try:
            photos = os.listdir(
                f"./media/{files[0]}")  # Используется files[0] для того, чтобы при вызове функции всегда отправлялся 1-ый файл
        except Exception as e:
            print(f"Ошибка выбора папки (возможно они закончились): {e}")

        # Создание пустого списка для заполнения его путями отправляемых фотографий
        media = []

        # Перебор фотографий в папке
        for i in photos:
            media.append(f"./media/{files[0]}/{i}")

        # Отправка фотографий
        try:
            await client.send_file(forum, media, reply_to=rep)
            # await client.send_file(forum2, media, reply_to=rep2)
        except Exception as e:
            print(f"Ошибка отправки фотографий: {e}")

        # Удаление отправленных фото для освобождения места
        try:
            for i in photos:
                os.remove(f"./media/{files[0]}/{i}")
            os.rmdir(f"./media/{files[0]}")
        except Exception as e:
            print(f"Ошибка удаления файлов: {e}")


    async def send_text():
        try:
            try:
                # Передаю в переменную json с текстами сообщений
                with open("text.json", "r", encoding="utf-8") as file:
                    messages = json.load(file)
            except:
                # Передаю в переменную json с текстами сообщений
                with open("text.json") as file:
                    messages = json.load(file)
        except Exception as e:
            print(f"Ошибка открытия файла (возможно закончились или из-за кодировки): {e}")

        try:
            # Отправка поста с текстом
            await client.send_message(forum, messages["message"][0]["text"], reply_to=rep)
            # await client.send_message(forum2, messages["message"][0]["text"], reply_to=rep2)
        except Exception as e:
            print(f"Ошибка отправки текстового поста: {e}")

        # Удаление из json-a отправленного текста
        del messages["message"][0]

        # Запись json-a обратно в файл
        with open("text.json", "w") as file:
            json.dump(messages, file, ensure_ascii=False, indent=2)


    async def send_channel():
        try:
            # Отправка поста с текстом
            await client.send_message(forum, "Переходите в мой телеграм канал!\n\nhttps://t.me/pamiatnikrf",
                                      reply_to=rep)
            # await client.send_message(forum2, "Переходите в мой телеграм канал!\n\nhttps://t.me/pamiatnikrf", reply_to=rep2)
        except Exception as e:
            print(f"Ошибка отправки поста с каналом: {e}")


    async def send_contacts():
        try:
            # Отправка поста с текстом
            await client.send_message(forum,
                                      "По вопросам сотрудничества пожалуйста пишите мне напрямую\n\nhttps://t.me/Eoblonski",
                                      reply_to=rep)
            # await client.send_message(forum2,
            #                           "По вопросам сотрудничества пожалуйста пишите мне напрямую\n\nhttps://t.me/Eoblonski",
            #                           reply_to=rep2)
        except Exception as e:
            print(f"Ошибка отправки поста с контактами: {e}")


    # Бесконечный цикл отправки сообщений через время
    while True:
        time_now = pytz.timezone('Europe/Moscow').localize(datetime.now()).strftime('%H:%M')
        sleep(waiting_to_wake_up(time_now, first_send_media))
        client.loop.run_until_complete(send_media())

        time_now = pytz.timezone('Europe/Moscow').localize(datetime.now()).strftime('%H:%M')
        sleep(waiting_to_wake_up(time_now, text_post))
        client.loop.run_until_complete(send_text())

        time_now = pytz.timezone('Europe/Moscow').localize(datetime.now()).strftime('%H:%M')
        sleep(waiting_to_wake_up(time_now, channel))
        client.loop.run_until_complete(send_channel())

        time_now = pytz.timezone('Europe/Moscow').localize(datetime.now()).strftime('%H:%M')
        sleep(waiting_to_wake_up(time_now, contacts))
        client.loop.run_until_complete(send_contacts())

        time_now = pytz.timezone('Europe/Moscow').localize(datetime.now()).strftime('%H:%M')
        sleep(waiting_to_wake_up(time_now, second_send_media))
        client.loop.run_until_complete(send_media())