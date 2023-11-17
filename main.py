

#bot = Bot(token="6597665670:AAEJAwxR08H32eZCqJqrQqKyiO8H-XLICsc")
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.types import ChatPermissions, BotCommandScopeAllPrivateChats, BotCommand
import asyncpg
import sqlite3
from datetime import datetime, timedelta
from LolzteamApi import LolzteamApi, Types
from aiogram.utils import exceptions
from aiogram.types import Dice, CallbackQuery

from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.contrib.fsm_storage.memory import MemoryStorage
import uuid

import json
import time

import random

import os


json_file_path = 'C:/Users/sovanedev/Desktop/e320tgbot/agreed_users.json'

API_TOKEN = "6597665670:AAEJAwxR08H32eZCqJqrQqKyiO8H-XLICsc"
DATABASE_URL = 'C:/Users/sovanedev/Desktop/e320tgbot/db.db'

home_path = '/home/debian/tge320'
json_file_path = os.path.join(home_path, 'agreed_users.json')
DATABASE_URL = os.path.join(home_path, 'db.db')

os.makedirs(os.path.dirname(json_file_path), exist_ok=True)
os.makedirs(os.path.dirname(DATABASE_URL), exist_ok=True)

#e320_id = -1002047946378 #test
e320_id = -1001550842546 #osnova
crut_id = [670017160, 6388329805]
ludik_id = -1002006881495 # ludik

current_period = "11\.11\.23 \- 01\.12\.23"

lzt = LolzteamApi(token='1e2ab991b144467ccaf20900faa3a3a056520bfc')

storage = MemoryStorage()
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot, storage=storage)
Bot.set_current(bot)
#
# creat
#


async def is_admin(victim_id):
    query = "SELECT * FROM staff WHERE user_id = ?"
    cursor.execute(query, (victim_id,))
    adm = cursor.fetchall()
    if adm or await is_creator(victim_id):
        return True
    else:
        return False
    
async def is_creator(victim_id):
    query = "SELECT * FROM creators WHERE user_id = ?"
    cursor.execute(query, (victim_id,))
    creat = cursor.fetchall()

    if creat:
        return True
    else:
        return False
    
@dp.message_handler(commands=['makestaff'])
async def cmd_makestaff(message: types.Message):
    if message.chat.type != types.ChatType.SUPERGROUP and message.chat.type != types.ChatType.GROUP:
        await message.reply("Эта команда может быть использована только в групповых чатах.")
        return
    
    admin = await bot.get_chat_member(e320_id, message.from_user.id)
    admin_id = message.from_user.id
    
    user = await bot.get_chat_member(e320_id, message.reply_to_message.from_user.id)
    user_id = message.reply_to_message.from_user.id

    if not admin_id in crut_id:
        await message.reply("Недостаточно прав.")
        return

    if await is_admin(user_id):
        await message.reply("Пользователь уже имеет полномочия.")
        return

    query = "INSERT INTO staff (user_id) VALUES (?)"
    cursor.execute(query, (user_id,))
    conn.commit()

    await bot.promote_chat_member(chat_id=e320_id, user_id=user_id, can_delete_messages=True, can_manage_chat=True, can_pin_messages=True)

    await bot.set_chat_administrator_custom_title(e320_id, user_id, "staff")

    admin_mention = admin.user.get_mention()
    user_mention = user.user.get_mention()

    await message.reply(f"{admin_mention} назначил пользователя {user_mention} модератором\.", parse_mode="MarkdownV2")


@dp.message_handler(commands=['unmakestaff'])
async def cmd_unmakestaff(message: types.Message):
    if message.chat.type != types.ChatType.SUPERGROUP and message.chat.type != types.ChatType.GROUP:
        await message.reply("Эта команда может быть использована только в групповых чатах.")
        return
    
    admin = await bot.get_chat_member(e320_id, message.from_user.id)
    admin_id = message.from_user.id
    
    user = await bot.get_chat_member(e320_id, message.reply_to_message.from_user.id)
    user_id = message.reply_to_message.from_user.id

    if not admin_id in crut_id:
        await message.reply("Недостаточно прав.")
        return

    if not await is_admin(user_id):
        await message.reply("Пользователь не имеет прав.")
        return
    
    query = "DELETE FROM staff WHERE user_id = ?"
    cursor.execute(query, (user_id,))

    if user.status in ["administrator"]:
        await bot.restrict_chat_member(chat_id=e320_id, user_id=user_id, can_delete_messages=False, can_manage_chat=False, can_pin_messages=False, can_add_web_page_previews=False)

    admin_mention = admin.user.get_mention()
    user_mention = user.user.get_mention()

    await message.reply(f"{admin_mention} разжаловал модератора {user_mention}\.", parse_mode="MarkdownV2")


@dp.message_handler(commands=['getid'])
async def cmd_getid(message: types.Message):
    if message.chat.type != types.ChatType.SUPERGROUP and message.chat.type != types.ChatType.GROUP:
        await message.reply("Эта команда может быть использована только в групповых чатах.")
        return
    
    admin = await bot.get_chat_member(e320_id, message.from_user.id)
    admin_id = message.from_user.id
    
    user_id = message.reply_to_message.from_user.id

    await message.reply(f"Айди: `{user_id}`", parse_mode="MarkdownV2") 

@dp.message_handler(commands=['makecreat'])
async def cmd_makecreat(message: types.Message):
    if message.chat.type != types.ChatType.SUPERGROUP and message.chat.type != types.ChatType.GROUP:
        await message.reply("Эта команда может быть использована только в групповых чатах.")
        return
    
    admin = await bot.get_chat_member(e320_id, message.from_user.id)
    admin_id = message.from_user.id
    
    user = await bot.get_chat_member(e320_id, message.reply_to_message.from_user.id)
    user_id = message.reply_to_message.from_user.id

    if not admin_id in crut_id:
        await message.reply("Недостаточно прав.")
        return

    if await is_creator(user_id):
        await message.reply("Пользователь уже имеет высшие полномочия.")
        return
    
    query = "INSERT INTO creators (user_id) VALUES (?)"
    cursor.execute(query, (user_id,))
    conn.commit()

    admin_mention = admin.user.get_mention()
    user_mention = user.user.get_mention()

    await message.reply(f"{admin_mention} назначил пользователя {user_mention} блатным\.", parse_mode="MarkdownV2")

@dp.message_handler(commands=['unmakecreat'])
async def cmd_unmakecreat(message: types.Message):
    if message.chat.type != types.ChatType.SUPERGROUP and message.chat.type != types.ChatType.GROUP:
        await message.reply("Эта команда может быть использована только в групповых чатах.")
        return
    
    admin = await bot.get_chat_member(e320_id, message.from_user.id)
    admin_id = message.from_user.id
    
    try:
        user = await bot.get_chat_member(e320_id, message.reply_to_message.from_user.id)
    except:
        print(f"{admin.user.get_mention()} попытался использовать /unmakecreat")
    user_id = message.reply_to_message.from_user.id

    if not admin_id in crut_id:
        await message.reply("Недостаточно прав.")
        return

    if not await is_creator(user_id):
        await message.reply("Пользователь не имеет прав.")
        return
    
    query = "DELETE FROM creators WHERE user_id =  ?"
    cursor.execute(query, (user_id,))

    admin_mention = admin.user.get_mention()
    user_mention = user.user.get_mention()

    await message.reply(f"{admin_mention} разжаловал администратора {user_mention}\.", parse_mode="MarkdownV2")

################################################################
## moder
################################################################

@dp.message_handler(commands=['ban'])
async def cmd_ban(message: types.Message):
    if message.chat.type != types.ChatType.SUPERGROUP and message.chat.type != types.ChatType.GROUP:
        await message.reply("Эта команда может быть использована только в групповых чатах.")
        return
    
    admin = await bot.get_chat_member(e320_id, message.from_user.id)
    admin_id = message.from_user.id
    
    if not message.reply_to_message:
        await message.reply("На кого вы хотите применить сообщение? ((ответь на него бля)).")
        return
    
    user = await bot.get_chat_member(e320_id, message.reply_to_message.from_user.id)
    user_id = message.reply_to_message.from_user.id
    
    if not await is_creator(admin_id):
        await message.reply("Недостаточно прав.")
        return
    
    if await is_admin(user_id):
        await message.reply("Данный пользователь является модератором.")
        return

    _, dur, *reason = message.text.split()
    reason = ' '.join(reason)

    await bot.ban_chat_member(e320_id, user_id=user_id)

    await message.reply(f"Пользователь @{user.user.username} был заблокирован в чате. Причина: {reason}")




async def mute_user(user_id, mute_time, unmute_time, reason, admin):
    user = await bot.get_chat_member(e320_id, user_id)

    permissions = ChatPermissions(
        can_send_messages=False
    )

    await bot.restrict_chat_member(e320_id, user_id, permissions)

    query = "INSERT INTO mute_list (user_id, mute_time, unmute_time, reason, admin) VALUES (?, ?, ?, ?, ?)"
    values = (user_id, mute_time, unmute_time, reason, admin)
    conn.execute(query, values)
    conn.commit()

async def unmute_users():
    try:
        while True:
            cur_time = datetime.now()

            query = "SELECT user_id, mute_time, unmute_time, reason, admin FROM mute_list WHERE unmute_time <= ?"
            records = conn.execute(query, (cur_time,)).fetchall()

            for record in records:
                user_id, _, _, _, _ = record
                print(user_id)
                try:
                    member = await bot.get_chat_member(e320_id, user_id)
                    await bot.promote_chat_member(e320_id, user_id, can_post_messages=True)
                    mention = member.user.get_mention()
                    await bot.send_message(e320_id, f"Пользователь {mention} был размучен по истечении времени\.", parse_mode="MarkdownV2")
                except Exception as member_error:
                    await send_log(str(member_error) + f"Failed to handle user_id: {user_id}")

            query = "DELETE FROM mute_list WHERE unmute_time <= ?"
            conn.execute(query, (cur_time,))
            conn.commit()
            await asyncio.sleep(2)
    except Exception as ex:
        await send_log(str(ex))

@dp.message_handler(commands=['mute'])
async def cmd_mute(message: types.Message):
    if message.chat.type != types.ChatType.SUPERGROUP and message.chat.type != types.ChatType.GROUP:
        await message.reply("Эта команда может быть использована только в групповых чатах.")
        return
    
    admin = await bot.get_chat_member(e320_id, message.from_user.id)
    admin_id = message.from_user.id
    
    if not message.reply_to_message:
        await message.reply("На кого вы хотите применить сообщение? ((ответь на него бля)).")
        return

    user = await bot.get_chat_member(e320_id, message.reply_to_message.from_user.id)
    user_id = message.reply_to_message.from_user.id

    if not await is_admin(admin_id):
        await message.reply("Недостаточно прав.")
        return
    
    if await is_admin(user_id):
        await message.reply("Данный пользователь является модератором.")
        return

    _, duration, *reason = message.text.split()
    reason = ' '.join(reason)

    if not message.reply_to_message or not message.reply_to_message.from_user:
        await message.reply("Не удалось определить пользователя.")
        return
    
    query = "SELECT user_id FROM mute_list WHERE user_id = ?"
    records = conn.execute(query, (user_id,)).fetchall()

    if records:
        await message.reply("Данный пользователь уже замучен.")
        return
    
    cur_time = datetime.now()

    mention = user.user.get_mention()

    try:
        user_id = message.reply_to_message.from_user.id

        unmute_time = cur_time + timedelta(seconds=int(parse_duration(str(duration))))

        if not reason:
            reason = "Не указана"
        await mute_user(user_id, cur_time, unmute_time, reason, message.from_user.id)

        if duration.isdigit():
            await message.reply(f"{mention} замучен на {duration} секунд\. Причина: {reason}", "MarkdownV2")
        else:
            await message.reply(f"{mention} замучен на {get_delta(str(duration))} Причина: {reason}", "MarkdownV2")
        await send_log(f"{mention} был замучен администратором {admin.user.get_mention()} на {get_delta(str(duration)) or duration}\. Причина: {reason}")
    except:
        message.reply("Неверный формат времени. hhmmss")
        return

async def unmute_user(victim_id, admin_id):
    await bot.promote_chat_member(e320_id, victim_id, can_post_messages=True)
    query = "DELETE FROM mute_list WHERE user_id = ?"
    conn.execute(query, (victim_id,))
    conn.commit()

@dp.message_handler(commands=['unmute'])
async def cmd_unmute(message: types.Message):
    if message.chat.type != types.ChatType.SUPERGROUP and message.chat.type != types.ChatType.GROUP:
        await message.reply("Эта команда может быть использована только в групповых чатах.")
        return
    
    admin = await bot.get_chat_member(e320_id, message.from_user.id)
    admin_id = message.from_user.id

    if not message.reply_to_message:
        await message.reply("Для использования команды - отправьте ее с ответом на target.")
    
    user_id = message.reply_to_message.from_user.id
    chat_member = await bot.get_chat_member(message.chat.id, user_id)

    if not await is_admin(admin_id):
        await message.reply("Недостаточно прав.")
        return

    if len(message.text.split()) > 5:
        await message.reply("Используйте команду следующим образом: /unmute причина")
        return

    if not message.reply_to_message or not message.reply_to_message.from_user:
        await message.reply("Не удалось определить пользователя.")
        return
    
    query = "SELECT user_id FROM mute_list WHERE user_id = ?"
    records = conn.execute(query, (user_id,)).fetchall()

    if not records:
        await message.reply("Данный пользователь не находится в муте и может отправлять сообщения.")
        return

    await unmute_user(user_id, message.from_user.id)

    mention = chat_member.user.get_mention()
    adm_mention = admin.user.get_mention()

    await message.reply(f"{mention} был размучен администратором {adm_mention} по причине: {' '.join(message.text.split()[1:]) if message.text.split()[1:] else 'Не указано'}", parse_mode="MarkdownV2")

################################################################
## welcome
################################################################

lztranks = {
    1: 'Гость', 
    2: 'Зарегистрирован',
    3: 'Администратор',
    4: 'Модератор', 
    7: 'Разработчик',
    8: 'Суприм', 
    9: 'Дизайнер',
    11: 'Продавец',
    12: 'Главный Модератор',
    18: '20 баллов',
    21: 'Местный',
    22: 'Постоялец',
    23: 'Эксперт',
    26: 'Легенда',
    29: 'Куратор',
    30: 'Арбитр',
    32: 'Бот',
    38: 'Антипаблик',
    41: 'Доступ к маркету',
    60: 'Гуру',
    65: 'Привилегии на маркете',
    142: 'read only', 
    166: 'Scam', 
    265: 'Уник', 
    349: 'Редактор', 
    350: 'Главный Дизайнер', 
    351: 'Искуственный Интеллект', 
    353: 'Главный Арбитр', 
    354: 'Рекламный Менеджер', 
    359: 'Спонсор', 
    360: 'Обжалование бана', 
    361: 'Команда Гарант-бота',
    365: 'Редактор',
}

async def welcome_message(new_members):
    for member in new_members:
        user_id = member.id
        user = await bot.get_chat_member(e320_id, user_id)
        
        if not user.user.is_bot:
            mention = user.user.get_mention()

            await bot.send_message(e320_id, f"{mention}, добро пожаловать в наш уютный чатик:\>", parse_mode="MarkdownV2")

            profile = lzt.forum.users.search(custom_fields={"telegram": user.user.username})
            
            tosend_text = ""
            if profile['users']:
                profile = profile['users'][0]
                tosend_text += f"Ссылка: <a href=\"{profile['links']['permalink']}\"> Профиль</a>\n"
                tosend_text += f"ID: <code>{profile['user_id']}</code>\n"
                tosend_text += f"Симпатии: {profile['user_like_count']}\n"
                tosend_text += f"Группа: {lztranks[profile['user_group_id']]}\n"
                datetime_object = datetime.utcfromtimestamp(profile['user_register_date'])
                reg_time = datetime_object.strftime('%Y-%m-%d')

                time_elapsed = datetime.utcnow() - datetime.utcfromtimestamp(profile['user_register_date'])
                elapsed_days = time_elapsed.days
                tosend_text += f"Дата регистрации: {reg_time} ({elapsed_days} д. назад)"
            else:
                tosend_text += "Профиль на zelenka.guru - не найден."
            await bot.send_message(e320_id, tosend_text, parse_mode="HTML")


@dp.message_handler(content_types=types.ContentType.NEW_CHAT_MEMBERS)
async def on_new_chat_members(message: types.Message):
    if message.chat.id == e320_id:
        await welcome_message(message.new_chat_members)

################################################################
## funny
################################################################

@dp.message_handler(commands=["setprefix"])
async def setprefix(message: types.Message):
    admin = await bot.get_chat_member(e320_id, message.from_user.id)
    admin_id = message.from_user.id

    user = await bot.get_chat_member(e320_id, message.reply_to_message.from_user.id)
    user_id = message.reply_to_message.from_user.id

    if not message.reply_to_message:
        await bot.send_message("Упомяните сообщение target.")

    if not await is_admin(admin_id):
        await message.reply("Недостаточно прав.")
        return

    prefix = " ".join(message.text.split()[1:])
    if not user.status in["administrator"]:
        await bot.promote_chat_member(e320_id, user_id, can_invite_users=True)

    await bot.set_chat_administrator_custom_title(e320_id, user_id, prefix)

    await message.reply(f"{admin.user.get_mention()} установил префикс для {user.user.get_mention()}: {prefix}", parse_mode="MarkdownV2")


async def count_messages(user_id):
    cursor.execute("SELECT message_count FROM message_top WHERE user_id=?", (user_id,))
    row = cursor.fetchone()

    if row:
        new_count = row[0] + 1
        cursor.execute("UPDATE message_top SET message_count=? WHERE user_id=?", (new_count, user_id))
    else:
        cursor.execute("INSERT INTO message_top (user_id, message_count) VALUES (?, 1)", (user_id,))
    
    conn.commit()

@dp.message_handler(commands=['top10'])
async def command_top_10(message: types.Message):

    cursor.execute("SELECT user_id, message_count FROM message_top ORDER BY message_count DESC LIMIT 10")
    top_users = cursor.fetchall()

    if top_users:
        top_users_text = "Топ 10 пользователей по сообщениям:\n"
        for index, (user_id, message_count) in enumerate(top_users, start=1):
            user_info = await bot.get_chat_member(e320_id, user_id)
            
            escaped_username = user_info.user.username.replace('_', r'\_') if user_info.user.username else "Удалён"
            user_name = f"[{escaped_username}](https://t.me/{escaped_username})" if user_info.user.username else f"Удалён"

            top_users_text += f"{index}\. {user_name} \- {message_count} сообщений\n"

        await message.reply(top_users_text, parse_mode="MarkdownV2", disable_web_page_preview=True, disable_notification=True, )
    else:
        await message.reply("В базе данных нет информации о сообщениях пользователей.")

@dp.message_handler(commands=["cleartop"])
async def cleartop(message: types.Message):
    admin = await bot.get_chat_member(e320_id, message.from_user.id)
    admin_id = message.from_user.id

    if not await is_creator(admin_id):
        await message.reply("Недостаточно прав.")
        return
    
    cursor.execute("SELECT user_id, message_count FROM message_top ORDER BY message_count DESC LIMIT 5")
    top_users = cursor.fetchall()

    if top_users:
        top_users_text = "Топ 3 самых активных пользователя:\n"
        index = 1
        for user_id, message_count in top_users:
            if index > 3:
                break
            if user_id in crut_id:
                continue
            
            user_info = await bot.get_chat_member(e320_id, user_id)
            
            escaped_username = user_info.user.username.replace('_', r'\_')
            user_name = f"[{escaped_username}](https://t.me/{escaped_username})" if user_info.user.username else f"{user_info.user.full_name}"

            top_users_text += f"{index}\. {user_name} \- {message_count} сообщений\n"
            index += 1
            
            
        await message.reply("Топ успешно очищен\. Топ 3 пользователя \- " + top_users_text, parse_mode="MarkdownV2", disable_web_page_preview=True)
    else:
        await message.reply("В базе данных нет информации о сообщениях пользователей.")
        return
    
    conn.execute("DELETE FROM message_top")
    conn.commit()

@dp.message_handler(commands=['lzt'])
async def lztprofile(message: types.Message):
    sender = await bot.get_chat_member(e320_id, message.from_user.id)
    sender_id = message.from_user.id

    if not message.reply_to_message:
        user = sender
    else:
        user = await bot.get_chat_member(e320_id, message.reply_to_message.from_user.id)
        user_id = sender_id
    
    if not user.user.is_bot:
        mention = user.user.get_mention()

        profile = lzt.forum.users.search(custom_fields={"telegram": user.user.username})
        
        tosend_text = ""
        if profile['users']:
            profile = profile['users'][0]
            tosend_text += f"| Ник: <a href=\"{profile['links']['permalink']}\"> {profile['username']}</a>\n"
            tosend_text += f"| ID: <code>{profile['user_id']}</code>\n"
            tosend_text += f"| Симпатии: {profile['user_like_count']}\n"
            tosend_text += f"| Группа: {lztranks[profile['user_group_id']]}\n"
            datetime_object = datetime.utcfromtimestamp(profile['user_register_date'])
            reg_time = datetime_object.strftime('%Y-%m-%d')

            time_elapsed = datetime.utcnow() - datetime.utcfromtimestamp(profile['user_register_date'])
            elapsed_days = time_elapsed.days
            tosend_text += f"| Дата регистрации: {reg_time} ({elapsed_days} д. назад)\n"

            #tosend_text += f"| Scammers: {'да' if scam else 'нет'}"
        else:
            tosend_text += "Профиль не найден."
        
        await bot.send_message(e320_id, tosend_text, "HTML", disable_web_page_preview=True, protect_content=True)

@dp.message_handler(commands=['rules'])
async def rules(message: types.Message):
    content = """
❗️Запрещается разжигание межнациональной розни. \n
❗️Запрещена политика в любом её виде. \n
❗️Запрещено неадекватное поведение. \n
❗️Несогласованная реклама - мут. Неоднократно - бан. \n
❗️Выпрашивание спонса - мут. Неоднократно - бан. \n
    """
    await message.reply(content)

#
#
#

giveaway_data = {}

@dp.message_handler(commands=['giveaway'])
async def giveaway(message: types.Message):
    sender = await bot.get_chat_member(e320_id, message.from_user.id)
    sender_id = message.from_user.id

    sent_message = await bot.send_message(e320_id, text="Ожидание..")
    giveaway_id = sent_message.message_id

    txt = message.text.split()
    if len(txt) < 4:
        content = "Невозможно создать розыгрыш, недостаточно аргументов\. time, count, desc"
        await bot.edit_message_text(content, chat_id=e320_id, message_id=giveaway_id, parse_mode="MarkdownV2")
        return
    raw_time, gift, desc = txt[1], txt[2], ' '.join(txt[3:])

    time_components = {'h': 0, 'm': 0, 's': 0}
    current_component = ''
    for char in raw_time:
        if char.isdigit():
            current_component += char
        else:
            if char in time_components:
                time_components[char] = int(current_component)
                current_component = ''

    total_seconds = (
        time_components['h'] * 3600 +
        time_components['m'] * 60 +
        time_components['s']
    )

    if total_seconds < 10:
        content = "Невозможно создать розыгрыш, время проведения < времени инициализации\."
        await bot.edit_message_text(content, chat_id=e320_id, message_id=giveaway_id, parse_mode="MarkdownV2")
        return

    end_of_contest = datetime.now() + timedelta(
        hours=time_components['h'], minutes=time_components['m'], seconds=time_components['s']
    )

    content = ""
    
    # Сохраняем данные о розыгрыше
    giveaway_data[giveaway_id] = {
        'end_of_contest': end_of_contest,
        'participants': set(),
        'creator_id': int(sender_id),
        'desc': desc,
        'gift': gift,
    }

    if end_of_contest and gift and desc:
        content += f"Новый розыгрыш от {sender.user.get_mention()}:\n"
        content += f"Закончится через {format_timedelta(end_of_contest - datetime.now())}\n"
        content += f"Количество: {gift}\n"
        content += f"Описание: {desc}\n"
        content += f"Участников: 0"

        # Добавим кнопки
        keyboard = types.InlineKeyboardMarkup()
        keyboard.add(types.InlineKeyboardButton(text="Обновить", callback_data=f"update_{giveaway_id}"))
        keyboard.add(types.InlineKeyboardButton(text="Принять участие", callback_data=f"join_{giveaway_id}"))

    query = "SELECT user_id FROM giveaway_auto"
    participants_from_db = [user[0] for user in cursor.execute(query).fetchall() if user[0] != sender_id]

    for k, v in giveaway_data.items():
        v['participants'].update(participants_from_db)

    await bot.edit_message_text(content, chat_id=e320_id, message_id=giveaway_id, parse_mode="MarkdownV2", reply_markup=keyboard)

def format_timedelta(delta):
    seconds = delta.seconds
    hours, remainder = divmod(seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    return f"{hours} ч\., {minutes} м\., {seconds} с\."


# Добавим обработчик для кнопок
@dp.callback_query_handler(lambda c: c.data.startswith(('join_')))
async def handle_button_join(callback_query: types.CallbackQuery):
    action, giveaway_id = callback_query.data.split('_')
    giveaway_id = int(giveaway_id)
    sender_id = callback_query.from_user.id

    if giveaway_id not in giveaway_data:
        await bot.answer_callback_query(callback_query.id, text="Розыгрыш не найден.")
        return

    if sender_id == giveaway_data[giveaway_id]['creator_id']:
        await bot.answer_callback_query(callback_query.id, text="Вы не можете принимать участие в своем собственном розыгрыше.")
        return
    
    query = "SELECT user_id FROM giveawayban_list WHERE user_id = ?"
    records = conn.execute(query, (sender_id,)).fetchall()

    if records:
        await bot.answer_callback_query(callback_query.id, text="Вы получили блокировку и не можете принимать участие в розыгрышах.")
        return

    if sender_id in giveaway_data[giveaway_id]['participants']:
        await bot.answer_callback_query(callback_query.id, text="Вы уже приняли участие в этом розыгрыше.")
    else:
        giveaway_data[giveaway_id]['participants'].add(sender_id)
        await bot.answer_callback_query(callback_query.id, text="Вы успешно приняли участие в розыгрыше.")
        sender = await bot.get_chat_member(e320_id, sender_id)
        await bot.send_message(e320_id, f"{sender.user.get_mention()} \- принял участие в розыгрыше\.", parse_mode="MarkdownV2")

@dp.callback_query_handler(lambda c: c.data.startswith('update_'))
async def handle_update_button(callback_query: types.CallbackQuery):
    action, giveaway_id = callback_query.data.split('_')
    giveaway_id = int(giveaway_id)
    sender_id = callback_query.from_user.id

    if giveaway_id not in giveaway_data:
        await bot.answer_callback_query(callback_query.id, text="Розыгрыш не найден.")
        return
    
    query = "SELECT user_id FROM giveawayban_list WHERE user_id = ?"
    records = conn.execute(query, (sender_id,)).fetchall()

    if records:
        await bot.answer_callback_query(callback_query.id, text="Вы получили блокировку и не можете принимать участие в розыгрышах.")
        return
    
    time_until_end = giveaway_data[giveaway_id]['end_of_contest'] - datetime.now()

    if time_until_end <= timedelta(seconds=3):
        await bot.answer_callback_query(callback_query.id, text="До конца розыгрыша осталось менее 3 секунд. Обновление невозможно.")
        return

    new_content = ""

    creator = await bot.get_chat_member(e320_id, giveaway_data[giveaway_id]['creator_id'])
    creator_mention = creator.user.get_mention()
    new_content += f"Новый розыгрыш от {creator_mention}:\n"
    new_content += f"Закончится через {format_timedelta(giveaway_data[giveaway_id]['end_of_contest'] - datetime.now())}\n"
    new_content += f"Количество: {giveaway_data[giveaway_id]['gift']}\n"
    new_content += f"Описание: {giveaway_data[giveaway_id]['desc']}\n"
    new_content += f"Участников: {len(giveaway_data[giveaway_id]['participants'])}"

    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(types.InlineKeyboardButton(text="Обновить", callback_data=f"update_{giveaway_id}"))
    keyboard.add(types.InlineKeyboardButton(text="Принять участие", callback_data=f"join_{giveaway_id}"))

    try:
        if new_content != callback_query.message.text:
            await bot.edit_message_text(
                chat_id=callback_query.message.chat.id,
                message_id=callback_query.message.message_id,
                text=new_content,
                reply_markup=keyboard, parse_mode="MarkdownV2")
            await bot.answer_callback_query(callback_query.id, text="Сообщение обновлено.")
        else:
            await bot.answer_callback_query(callback_query.id, text="Изменений нет.")
    except:
        await bot.answer_callback_query(callback_query.id, text="Не так часто.")

def get_delta(time_str): # получает на вход 10h10m10s, возвращает 10ч. 10м. 10с
    time_components = {'h': 0, 'm': 0, 's': 0}
    current_component = ''
    delta = timedelta()

    print(time_str)

    for char in time_str:
        if char.isdigit():
            current_component += char
        else:
            if char in time_components:
                time_components[char] = int(current_component)
                current_component = ''

    delta += timedelta(hours=time_components['h'], minutes=time_components['m'], seconds=time_components['s'])
    print(delta)
    return format_timedelta(delta)


def parse_duration(duration_str): # получает на вход 10h10m10s возвращает секунды
    hours, minutes, seconds = 0, 0, 0

    duration_str = str(duration_str)

    # Split the string into parts
    parts = duration_str.split('h')

    # Process hours
    if len(parts) > 1:
        hours = int(parts[0])
        parts = parts[1]

    # If there's no 'h', split the remaining string into parts for minutes and seconds
    if 'm' in parts:
        parts = parts.split('m')

        # Process minutes
        if len(parts) > 1:
            minutes = int(parts[0])
            parts = parts[1]

            # Process seconds (handle 's' directly)
            if parts and parts.rstrip('s'):
                seconds = int(parts.rstrip('s'))
        else:
            # No 'm' found, assume the remaining string is in seconds
            if parts and parts.rstrip('s'):
                seconds = int(parts.rstrip('s'))
    else:
        # No 'h' found, so process the whole string for minutes and seconds
        if 'm' in duration_str:
            parts = duration_str.split('m')
            minutes = int(parts[0])

            # Process seconds (handle 's' directly)
            if len(parts) > 1 and parts[1].rstrip('s'):
                seconds = int(parts[1].rstrip('s'))
        else:
            # No 'm' found, assume the whole string is in seconds
            if duration_str.rstrip('s'):
                seconds = int(duration_str.rstrip('s'))

    # Calculate the total duration in seconds
    total_seconds = hours * 3600 + minutes * 60 + seconds
    return total_seconds


#
#
#

@dp.message_handler(commands=["giveban"])
async def cmd_giveban(message: types.Message):
    if message.chat.type != types.ChatType.SUPERGROUP and message.chat.type != types.ChatType.GROUP:
        await message.reply("Эта команда может быть использована только в групповых чатах.")
        return
    
    admin = await bot.get_chat_member(e320_id, message.from_user.id)
    admin_id = message.from_user.id

    if not message.reply_to_message:
        await message.reply("Для использования команды - отправьте ее с ответом на target.")
    
    user_id = message.reply_to_message.from_user.id
    chat_member = await bot.get_chat_member(message.chat.id, user_id)

    if not await is_admin(admin_id):
        await message.reply("Недостаточно прав.")
        return

    if len(message.text.split()) > 5:
        await message.reply("Используйте команду следующим образом: /giveban причина")
        return

    if not message.reply_to_message or not message.reply_to_message.from_user:
        await message.reply("Не удалось определить пользователя.")
        return
    
    query = "SELECT user_id FROM giveawayban_list WHERE user_id = ?"
    records = conn.execute(query, (user_id,)).fetchall()

    if records:
        await message.reply("Данный пользователь уже находится в бане и может участвовать в розыгрышах.")
        return
    
    query = "INSERT INTO giveawayban_list (user_id) VALUES (?)"
    conn.execute(query, (user_id,))
    conn.commit()

    await message.reply(f"Пользователь @{chat_member.user.username} больше не может участвовать в розыгрышах\. \nПричина: {' '.join(message.text.split()[1:])}", parse_mode="MarkdownV2")

@dp.message_handler(commands=["ungiveban"])
async def cmd_ungiveban(message: types.Message):
    if message.chat.type != types.ChatType.SUPERGROUP and message.chat.type != types.ChatType.GROUP:
        await message.reply("Эта команда может быть использована только в групповых чатах.")
        return
    
    admin = await bot.get_chat_member(e320_id, message.from_user.id)
    admin_id = message.from_user.id

    if not message.reply_to_message:
        await message.reply("Для использования команды - отправьте ее с ответом на target.")
    
    user_id = message.reply_to_message.from_user.id
    chat_member = await bot.get_chat_member(message.chat.id, user_id)

    if not await is_admin(admin_id):
        await message.reply("Недостаточно прав.")
        return

    if len(message.text.split()) > 10:
        await message.reply("Используйте команду следующим образом: /ungiveban")
        return

    if not message.reply_to_message or not message.reply_to_message.from_user:
        await message.reply("Не удалось определить пользователя.")
        return
    
    query = "SELECT user_id FROM giveawayban_list WHERE user_id = ?"
    records = conn.execute(query, (user_id,)).fetchall()

    if not records:
        await message.reply("Данный пользователь не находится в бане и может участвовать в розыгрышах.")
        return
    
    query = "DELETE FROM giveawayban_list WHERE user_id = ?"
    conn.execute(query, (user_id,))
    conn.commit()

    await message.reply(f"Пользователь @{chat_member.user.username} теперь может принимать участие в розыгрышах\.", parse_mode="MarkdownV2")

@dp.message_handler(commands=["makeau"])
async def cmd_ungiveban(message: types.Message):
    if message.chat.type != types.ChatType.SUPERGROUP and message.chat.type != types.ChatType.GROUP:
        await message.reply("Эта команда может быть использована только в групповых чатах.")
        return
    
    admin = await bot.get_chat_member(e320_id, message.from_user.id)
    admin_id = message.from_user.id
    
    user_id = message.reply_to_message.from_user.id
    chat_member = await bot.get_chat_member(message.chat.id, user_id)

    if not message.reply_to_message or not message.reply_to_message.from_user:
        await message.reply("Не удалось определить пользователя.")
        return

    if not await is_admin(admin_id):
        await message.reply("Недостаточно прав.")
        return
    
    query = "SELECT user_id FROM giveaway_auto WHERE user_id = ?"
    records = conn.execute(query, (user_id,)).fetchall()

    if records:
        await message.reply("Данный пользователь уже имеет АУ.")
        return
    
    query = "INSERT INTO giveaway_auto (user_id) VALUES (?)"
    conn.execute(query, (user_id,))
    conn.commit()

    mention = chat_member.user.get_mention()
    adm_mention = admin.user.get_mention()

    await message.reply(f"{mention} был добавлен в список АУ администратором {adm_mention}\.", parse_mode="MarkdownV2")
    
@dp.message_handler(commands=["uinfo"])
async def cmd_info(message: types.Message):
    sender = await bot.get_chat_member(e320_id, message.from_user.id)
    sender_id = message.from_user.id

    if not message.reply_to_message:
        user = sender
        user_id = sender_id
    else:
        user = await bot.get_chat_member(e320_id, message.reply_to_message.from_user.id)
        user_id = message.reply_to_message.from_user.id

    message_content = ''

    escaped_username = user.user.username.replace('_', r'\_') if user.user.username else "Удалён"

    if not user.user.is_bot:
        message_content += f"Информация о пользователе [{escaped_username}](https://t.me/{escaped_username}):\n"
        cursor.execute("SELECT message_count FROM message_top WHERE user_id=?", (user_id,))
        row = cursor.fetchone()
        if row:
            messages = row[0]
        message_content += f"Кол\-во сообщений за период \({current_period}\): {messages}\.\n"
        if await is_creator(user_id):
            message_content += f"Ранг пользователя: {'fd'}\.\n"
        elif await is_admin(user_id):
            message_content += f"Ранг пользователя: {'Администратор'}\.\n"
        else:
            message_content += f"Ранг пользователя: Отсутствует\.\n"
        cursor.execute("SELECT user_id FROM giveaway_auto WHERE user_id=?", (user_id,))
        row = cursor.fetchone()
        if row:
            message_content += f"Платное повышение прав: Автоучастие в розыгрышах\.\n"
        else:
            message_content += f"Платное повышение прав: Отсутствует\.\n"

        row = cursor.execute("SELECT gives_count FROM giveaway_count WHERE user_id= ?", (user_id,)).fetchone()

        if row is not None and row[0]:
            message_content += f"Кол\-во выигранных розыгрышей: {row[0]}\.\n"
        else:
            message_content += f"Кол\-во выигранных розыгрышей: 0\.\n"
        #message_content += f""

        await message.reply(message_content, "MarkdownV2", disable_web_page_preview=True)

@dp.message_handler(commands=["getbyid"])
async def cmd_getbyid(message: types.Message):
    admin = await bot.get_chat_member(e320_id, message.from_user.id)

    id = message.text.split()[1:]
    if not id: return

    user = await bot.get_chat_member(message.chat.id, int(''.join(id)))

    if not user:
        return

    await message.reply(text=f"@{user.user.username}")


#
# ludiki
#
@dp.message_handler(commands=["start"])
async def cmd_start(message: types.Message):
    if message.chat.type != 'private':
        return
    user_id = message.from_user.id

    politicy = "Нажимая кнопку Я согласен - Вы автоматически соглашаетесь с правилами нашего сервиса.\n"
    politicy += "Пополняя баланс бота Вы передаете ваши средства на хранение/использование/передачу, т.е прокрут денег в системе. Гарантируем вам возврат вашего баланса, в случае отсутствия денег на балансе.\n"
    politicy += "Администрация вправе отказать Вам в выводе Ваших средств в случае нарушения Правил сервиса без объяснения причин.\n"
    politicy += "В случае попытки обмана игроков - все Ваши средства могут быть заморожены, а Ваш аккаунт будет заблокирован.\n"
    politicy += "Данный бот выступает гарантом в \"костях\", т.е В случае вашего проигрыша и отказа от выплат - Администрация изымет средства с вашего баланса и передаст их Выигравшей стороне.\n"
    politicy += "От 16.11.2023 18:25:50"


    agreed = await has_user_agreed(user_id)
    if not agreed:
        keyboard = types.InlineKeyboardMarkup()
        keyboard.add(types.InlineKeyboardButton(text="Я согласен", callback_data=f"agree"))
        await bot.send_message(message.chat.id, text=f"Приветствую! Прежде чем продолжить, пожалуйста, прочтите нашу политику.\n {politicy}", reply_markup=keyboard)
        return
    
    query = "SELECT balance FROM ludik_balance WHERE user_id = ?"
    raw = cursor.execute(query, (user_id,)).fetchone()

    message_content = ""
    keyboard = None

    if raw:
        raw = raw[0]
        message_content += "Ваш профиль: \n"
        message_content += f"Баланс: {round(raw)} RUB\n"

        keyboard = types.InlineKeyboardMarkup()
        keyboard.add(types.InlineKeyboardButton(text="Пополнить баланс", callback_data=f"deposite"))
        keyboard.add(types.InlineKeyboardButton(text="Вывести средства", callback_data=f"withdraw"))
        keyboard.add(types.InlineKeyboardButton(text="Магазин", callback_data=f"shop"))
    else:
        query = "INSERT INTO ludik_balance (user_id, balance, count, wins, allwins) VALUES (?, 0, 0, 0, 0)"
        cursor.execute(query, (user_id,))
        conn.commit()
        message_content = "Аккаунт был создан."

    await bot.send_message(message.chat.id, text=message_content, reply_markup=keyboard)

async def has_user_agreed(user_id):
    agreed_users = read_agreed_users()
    return user_id in agreed_users

def read_agreed_users():
    try:
        with open(json_file_path, 'r') as file:
            agreed_users = json.load(file)
    except FileNotFoundError:
        agreed_users = {'users': []}
    return agreed_users.get('users', [])

def write_agreed_users(agreed_users):
    with open(json_file_path, 'w') as file:
        json.dump({'users': agreed_users}, file)

@dp.callback_query_handler(lambda c: c.data.startswith('agree'))
async def handle_agree_button(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    agreed_users = read_agreed_users()

    if user_id not in agreed_users:
        agreed_users.append(user_id)
        write_agreed_users(agreed_users)

    await bot.send_message(callback_query.message.chat.id, text="Теперь вы можете начать использование бота.")

    query = "SELECT balance FROM ludik_balance WHERE user_id = ?"
    raw = cursor.execute(query, (user_id,)).fetchone()
    keyboard = None

    message_content = ""

    if raw:
        raw = raw[0]
        message_content += "Ваш профиль: \n"
        message_content += f"Баланс: {round(raw)} RUB\n"

        keyboard = types.InlineKeyboardMarkup()
        keyboard.add(types.InlineKeyboardButton(text="Пополнить баланс", callback_data=f"deposite"))
        keyboard.add(types.InlineKeyboardButton(text="Вывести средства", callback_data=f"withdraw"))
        keyboard.add(types.InlineKeyboardButton(text="Магазин", callback_data=f"shop"))
    else:
        query = "INSERT INTO ludik_balance (user_id, balance, count, wins, allwins) VALUES (?, 0, 0, 0, 0)"
        cursor.execute(query, (user_id,))
        conn.commit()
        message_content = "Аккаунт был создан."

    await bot.send_message(callback_query.message.chat.id, text=message_content, reply_markup=keyboard)


def get_balance(user_id):
    query = "SELECT balance FROM ludik_balance WHERE user_id = ?"
    raw = cursor.execute(query, (user_id,)).fetchone()
    if not raw:
        return 0
    return raw[0]


@dp.message_handler(commands=["transfer"])
async def cmd_start(message: types.Message):
    if message.chat.type != 'private':
        return
    
    user_id = message.from_user.id

    _, reciver_id, summ = message.text.split()

    reciver_id = int(reciver_id)
    summ = int(summ)

    if not isinstance(summ, int) or int(summ) < 0:
        await bot.send_message(user_id, "Укажите сумму > 0, целым числом.")
        return

    if summ is None:
        await bot.send_message(user_id, "Неверно использована команда.  баланс")
        return
    
    if get_balance(user_id) < summ:
        await bot.send_message(user_id, "Недостаточно средств для перевода.")
        return
    
    reciver_get = get_balance(reciver_id) + summ
    user_get = get_balance(user_id) - summ

    query = "UPDATE ludik_balance SET balance = ? WHERE user_id = ?"
    cursor.execute(query, (user_get, user_id,))

    query = "UPDATE ludik_balance SET balance = ? WHERE user_id = ?"
    cursor.execute(query, (reciver_get, reciver_id,))

    username = await bot.get_chat_member(ludik_id, reciver_id)
    username = username.user.username

    await bot.send_message(user_id, f"Перевод на сумму {summ} RUB отправлен пользователю @{username}\.", parse_mode="MarkdownV2")
    await bot.send_message(reciver_id, f"Пополнение на сумму {summ} RUB получен от пользователя @{message.from_user.username}\.", parse_mode="MarkdownV2")

class Prefix(StatesGroup):
    waiting_for_deposit = State()
    waiting_for_prefix = State()

@dp.callback_query_handler(lambda c: c.data.startswith('shop'))
async def handle_deposite_button(callback_query: types.CallbackQuery, state: FSMContext):
    
    message_text = f"Автоучастие в розыгрышах - 250 рублей навсегда\n"
    message_text += f"Кастомный префикс - 15 рублей - навсегда"

    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(types.InlineKeyboardButton(text="Автоучастие", callback_data=f"auto"))
    keyboard.add(types.InlineKeyboardButton(text="Префикс", callback_data=f"prefix"))
    await bot.send_message(callback_query.from_user.id, message_text, reply_markup=keyboard)


@dp.callback_query_handler(lambda c: c.data == 'auto', state="*")
async def handle_auto_choice(callback_query: types.CallbackQuery, state: FSMContext):
    message_text = "Вы собираетесь приобрести Автоучастие."
    query = "SELECT balance FROM ludik_balance WHERE user_id = ?"
    raw = cursor.execute(query, (callback_query.from_user.id,)).fetchone()

    if raw[0] < 250:
        await bot.send_message(chat_id=callback_query.from_user.id, text="Недостаточно средств на балансе.")
        await state.finish()
        return
    
    query = "SELECT user_id FROM giveaway_auto WHERE user_id = ?"
    raw = cursor.execute(query, (callback_query.from_user.id,)).fetchone()

    if raw[0]:
        await bot.send_message(chat_id=callback_query.from_user.id, text="У вас уже приобретено Автоучастие.")
        await state.finish()
        return

    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(types.InlineKeyboardButton(text="Приобрести", callback_data="confirm_auto"))
    await bot.send_message(callback_query.from_user.id, message_text, reply_markup=keyboard)

    await Prefix.waiting_for_deposit.set()
    await state.update_data(choice='auto')


@dp.callback_query_handler(lambda c: c.data == 'prefix', state="*")
async def handle_prefix_choice(callback_query: types.CallbackQuery, state: FSMContext):
    message_text = "Введите желаемый префикс."

    query = "SELECT balance FROM ludik_balance WHERE user_id = ?"
    raw = cursor.execute(query, (callback_query.from_user.id,)).fetchone()

    if raw[0] < 15:
        await bot.send_message(chat_id=callback_query.from_user.id, text="Недостаточно средств на балансе.")
        await state.finish()
        return
    
    await bot.send_message(callback_query.from_user.id, message_text)

    await Prefix.waiting_for_prefix.set()


@dp.message_handler(state=Prefix.waiting_for_prefix)
async def handle_prefix_input(message: types.Message, state: FSMContext):
    user_input = message.text
    try:
        user = await bot.get_chat_member(e320_id, message.from_user.id)

        query = "SELECT balance FROM ludik_balance WHERE user_id = ?"
        raw = cursor.execute(query, (message.from_user.id,)).fetchone()[0]

        new_balance = raw - 15

        if not user.status in["administrator"]:
            await bot.promote_chat_member(e320_id, message.from_user.id, can_invite_users=True)

        await bot.set_chat_administrator_custom_title(e320_id, message.from_user.id, user_input)

        query = "UPDATE ludik_balance SET balance = ? WHERE user_id = ?"
        cursor.execute(query, (new_balance, message.from_user.id,))
        
        success_message = f"Префикс '{user_input}' успешно выдан."
        await bot.send_message(message.from_user.id, success_message)
    except Exception as ex:
        print(ex)
        await bot.send_message(message.from_user.id, "Произошла ошибка.")

    await state.finish()


@dp.callback_query_handler(lambda c: c.data == 'confirm_auto', state=Prefix.waiting_for_deposit)
async def handle_confirm_auto(callback_query: types.CallbackQuery, state: FSMContext):
    try:
        query = "SELECT balance FROM ludik_balance WHERE user_id = ?"
        raw = cursor.execute(query, (callback_query.from_user.id,)).fetchone()[0]

        new_balance = raw - 250

        query = "UPDATE ludik_balance SET balance = ? WHERE user_id = ?"
        cursor.execute(query, (new_balance, callback_query.from_user.id,))

        au_query = "INSERT INTO giveaway_auto (user_id) VALUES user_id = ?"
        cursor.execute(query, (callback_query.from_user.id,))

        success_message = "Покупка Автоучастия прошла успешно."
        await bot.send_message(callback_query.from_user.id, success_message)
    except Exception as ex:
        print(ex)
        await bot.send_message(callback_query.from_user.id, "Произошла ошибка.")

class Dep(StatesGroup):
    waiting_for_deposit = State()

@dp.callback_query_handler(lambda c: c.data.startswith('deposite'))
async def handle_deposite_button(callback_query: types.CallbackQuery, state: FSMContext):
    await Dep.waiting_for_deposit.set()
    
    deposit_key = str(uuid.uuid4())
    
    await DepositState.waiting_for_deposit_amount.set()
    await state.update_data(deposit_key=deposit_key)
    
    message_text = f"Введите сумму пополнения."
    await bot.send_message(callback_query.from_user.id, message_text)

class DepositState(StatesGroup):
    waiting_for_deposit_amount = State()
    waiting_for_deposit_key = State()
    waiting_for_payment_confirmation = State()

async def check_payment_confirmation(user_id, deposit_key):
    try:
        data = lzt.market.payments.history(user_id=6620542, comment=f"{user_id}{deposit_key}")
        print(data)
        return data['payments']
    except Exception as e:
        print(f"Error checking payment confirmation: {str(e)}")
        return None

async def wait_for_payment_confirmation(callback_query, state, user_id, deposit_key, timeout=300, check_interval=10):
    start_time = time.time()

    while time.time() - start_time < timeout:
        data = await check_payment_confirmation(user_id, deposit_key)

        if isinstance(data, dict):
            for key, value in data.items():
                if isinstance(value, dict):
                    print(f"value: {value}")
                    incoming_sum_value = value.get('incoming_sum')
                    print(incoming_sum_value)
                    if incoming_sum_value is not None:
                        break
            else:
                incoming_sum_value = None
        else:
            incoming_sum_value = None

        if incoming_sum_value is not None:
            await state.finish()
            get_amount_query = "SELECT balance FROM ludik_balance WHERE user_id = ?"
            row = cursor.execute(get_amount_query, (user_id,)).fetchone()
            if row:
                current_balance = row[0]
                new_balance = current_balance + (incoming_sum_value)
                update_query = "UPDATE ludik_balance SET balance = ? WHERE user_id = ?"
                cursor.execute(update_query, (new_balance, user_id))
                await callback_query.reply("Платеж подтвержден")

                return

        await asyncio.sleep(check_interval)

    await callback_query.answer("Время ожидания подтверждения платежа истекло.")
    await state.finish()



@dp.message_handler(state=DepositState.waiting_for_deposit_amount)
async def handle_deposit_amount(message: types.Message, state: FSMContext):
    try:
        deposit_amount = float(message.text)
        user_id = message.from_user.id
        
        data = await state.get_data()
        deposit_key = data.get('deposit_key')
        
        if not deposit_key:
            await message.answer("Произошла ошибка. Пожалуйста, начните заново.")
            await state.finish()
            return
        
        if deposit_amount <= 0:
            await message.answer("Только положительное число.")
            await state.finish()
            return

        url = f"https://zelenka.guru/payment/balance/transfer?hold=0&amount={deposit_amount}&username=sovanedev&comment={user_id}{deposit_key}" 

        task = asyncio.create_task(wait_for_payment_confirmation(callback_query=message, state=state, user_id=user_id, deposit_key=deposit_key))
        await state.update_data(task=task, depos="123")

        keyboard = types.InlineKeyboardMarkup()
        keyboard.add(types.InlineKeyboardButton(text="Оплатить", url=url))
        keyboard.add(types.InlineKeyboardButton(text="Отменить", callback_data='cancel_payment'))

        await message.answer(f"Ссылка для оплаты создана. Сумма с учетом комиссии: {deposit_amount}", reply_markup=keyboard)

    except ValueError:
        await message.answer("Пожалуйста, введите корректное число.")
    
@dp.callback_query_handler(lambda c: c.data == 'cancel_payment', state=DepositState.waiting_for_deposit_amount)
async def cancel_payment(callback_query: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    task = data.get('task')

    if task and not task.done():
        await task.cancel()
        await callback_query.answer("Оплата отменена.")
    else:
        await callback_query.answer("Нечего отменять.")

    await state.finish()

@dp.message_handler(commands=["balance"])
async def show_balance(message: types.Message):
    if message.chat.type != types.ChatType.SUPERGROUP and message.chat.type != types.ChatType.GROUP:
        await message.reply("Эта команда может быть использована только в групповых чатах.")
        return
    
    sender = await bot.get_chat_member(e320_id, message.from_user.id)
    sender_id = message.from_user.id
    
    if not message.reply_to_message:
        user = await bot.get_chat_member(e320_id, message.from_user.id)
        user_id = message.from_user.id
    else:
        user = await bot.get_chat_member(e320_id, message.reply_to_message.from_user.id)
        user_id = message.reply_to_message.from_user.id

    if not message.reply_to_message or not message.reply_to_message.from_user:
        await message.reply("Не удалось определить пользователя.")
        return
    
    balance = get_balance(user_id)

    await bot.send_message(message.chat.id, text=f"Баланс пользователя <a href=\"https://t.me/{user.user.username}\">{user.user.username}</a> составляет: {balance} RUB.", parse_mode="HTML", disable_web_page_preview=True)


async def get_user_id(username):
    try:
        user = await bot.get_chat(username)
        return user.id
    except Exception as e:
        print(f"Error getting user ID: {e}")
        return None

    
class Withdraw(StatesGroup):
    waiting_for_withdraw_amount = State()
    waiting_for_nickname = State()
    waiting_for_agree = State()

@dp.callback_query_handler(lambda c: c.data.startswith('withdraw'))
async def handle_withdraw_button(callback_query: types.CallbackQuery, state: FSMContext):
    await Withdraw.waiting_for_withdraw_amount.set()
    
    message_text = f"Введите сумму для вывода. Комиссия на вывод составляет: 1%."
    await bot.send_message(callback_query.from_user.id, message_text)

@dp.message_handler(state=Withdraw.waiting_for_withdraw_amount)
async def handle_withdraw_amount(message: types.Message, state: FSMContext):
    try:
        withdraw_amount = int(int(message.text)*1.01)
        user_id = message.from_user.id

        my_amount = lzt.market.profile.get()['user']['balance']

        query = "SELECT balance FROM ludik_balance WHERE user_id = ?"
        user_amount = cursor.execute(query, (user_id,)).fetchone()[0]

        if withdraw_amount <= 10:
            await bot.send_message(user_id, f"Вывод от 10 рублей.")

        if withdraw_amount > int(user_amount):
            await bot.send_message(user_id, f"На вашем балансе {user_amount}, Вы не можете вывести больше, чем у Вас есть.")
            await state.finish()
            return
        
        if int(withdraw_amount) > int(my_amount):
            await bot.send_message(user_id, "Выплаты временно приостановлены, на балансе обменника недостаточно денег.")
            await state.finish()
            return
        
        await state.update_data(withdraw_amount=withdraw_amount)
        
        await Withdraw.waiting_for_nickname.set()
        message_text = "Отправьте ваш никнейм на zelenka.guru"
        await bot.send_message(user_id, message_text)
        
    except ValueError:
        await message.answer("Пожалуйста, введите корректное число для вывода.")

@dp.message_handler(state=Withdraw.waiting_for_nickname)
async def handle_withdraw_nickname(message: types.Message, state: FSMContext):
    try:
        user_id = message.from_user.id
        nickname = message.text.strip()
        
        await state.update_data(nickname=nickname)
        
        await perform_withdrawal(user_id, state)
        
    except Exception as e:
        print(f"Error handling nickname: {str(e)}")
        await message.answer("Произошла ошибка при обработке вашего никнейма. Попробуйте снова.")
        return

async def perform_withdrawal(user_id, state):
    try:
        data = await state.get_data()
        withdraw_amount = data.get('withdraw_amount')
        nickname = data.get('nickname')
        
        withdrawal_link = f"Вы собираетесь вывести {withdraw_amount} рублей на https://zelenka.guru/{nickname}"
        
        await bot.send_message(user_id, withdrawal_link)

        await asyncio.sleep(2)
        
        await bot.send_message(user_id, "Все верно? (Да/Нет)")
        
        await Withdraw.next()
        
    except Exception as e:
        print(f"Error performing withdrawal: {str(e)}")
        await bot.send_message(user_id, "Произошла ошибка при выполнении вывода. Попробуйте снова.")
        await state.finish()

@dp.message_handler(state=Withdraw.waiting_for_agree)
async def handle_withdraw_confirmation(message: types.Message, state: FSMContext):
    try:
        user_id = message.from_user.id
        confirmation_response = message.text.strip().lower()

        if confirmation_response == 'да':

            data = await state.get_data()
            withdraw_amount = data.get('withdraw_amount')
            nickname = data.get('nickname')
            if withdraw_amount and nickname:
                result = lzt.market.payments.transfer(amount=withdraw_amount, secret_answer="sovanedev", currency=Types.Market.Currency.rub, username=nickname, comment=f"Вывод денег e320 Chatludik")
                if result:
                    await message.answer("Создали заявку на вывод. Спасибо за доверие!")
                    query = "SELECT balance FROM ludik_balance WHERE user_id = ?"
                    cur_balance = cursor.execute(query, (user_id,)).fetchone()[0]

                    query = "UPDATE ludik_balance SET balance = ? WHERE user_id = ?"
                    cursor.execute(query, (int(cur_balance) - int(withdraw_amount), user_id,))
                else:
                    await message.answer("Произошла ошибка при выполнении вывода. Пожалуйста, попробуйте снова.")
            else:
                await message.answer("Не удалось получить необходимые данные для вывода. Пожалуйста, начните процесс заново.")
        else:
            await message.answer("Ваш вывод был отменен.")
        
        await state.finish()

    except Exception as e:
        print(f"Error handling withdrawal confirmation: {str(e)}")
        await message.answer("Произошла ошибка при обработке вашего ответа. Попробуйте снова.")

################################################################
## count
################################################################

@dp.message_handler()
async def handle_message(message: types.Message):
    if message.chat.type != types.ChatType.SUPERGROUP and message.chat.type != types.ChatType.GROUP:
        return
    if message.chat.id != e320_id:
        return
    user_id = message.from_user.id
    await count_messages(user_id)

async def on_startup(dp):
    asyncio.create_task(unmute_users())
    asyncio.create_task(check_cont())

giveaways_file_path = "C:/Users/sovanedev/Desktop/e320tgbot/giveaways.json"

async def load_giveaways():
    try:
        with open(giveaways_file_path, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return {'contests': {}}

async def save_giveaways(giveaways_data):
    with open(giveaways_file_path, 'w') as file:
        json.dump(giveaways_data, file)

async def check_cont():
    to_remove = [] 

    #giveaways_data = await load_giveaways()

    while True:
        for giveaway_id, data in giveaway_data.items():
            if data["end_of_contest"] <= datetime.now():
                participants = list(giveaway_data[giveaway_id]['participants'])
                winners = random.sample(participants, min(int(giveaway_data[giveaway_id]['gift']), len(participants)))

                await send_log(str(giveaway_id) + str(data))

                winners_content = f"Розыгрыш закончен. Выбраны случайные участники:\n"
                for winner_id in winners:
                    winner_user = await bot.get_chat_member(e320_id, winner_id)
                    profile = lzt.forum.users.search(custom_fields={"telegram": winner_user.user.username})
                    try:
                        winners_content += f"@{winner_user.user.username} | <a href='{profile['users'][0]['links']['permalink']}'>lzt</a> \n"
                    except:
                        winners_content += f"@{winner_user.user.username}\n"
                    
                    query = "SELECT gives_count FROM giveaway_count WHERE user_id = ?"
                    cursor.execute(query, (winner_id,))
                    row = cursor.fetchone()
                    if row:
                        query = "UPDATE giveaway_count SET gives_count = ? WHERE user_id = ? "
                        cursor.execute(query, (int(row[0]+1), winner_id,))
                    else:
                        query = "INSERT INTO giveaway_count (user_id, gives_count) VALUES (?, 1)"
                        cursor.execute(query, (winner_id,))
                
                #giveaways_data['contests'][giveaway_id] = json.decoder(data)

                #await save_giveaways(giveaways_data)
                    
                await bot.edit_message_text(text=winners_content, chat_id=e320_id, message_id=giveaway_id, parse_mode="HTML")
                to_remove.append(giveaway_id)
                await bot.send_message(e320_id, text=f"<a href='https://t.me/e320_lzttalk/{giveaway_id}'> Розыгрыш</a> оконечен.", parse_mode="HTML")

        for key in to_remove:
            del giveaway_data[key]
            to_remove.remove(key)

        await asyncio.sleep(3)

async def send_log(e):
    try:
        await bot.send_message(chat_id=6388329805, text=str(e), parse_mode="MarkdownV2")
    except Exception as ex:
        await bot.send_message(chat_id=6388329805, text=str(e))


if __name__ == '__main__':
    from aiogram import executor

    send_log(DATABASE_URL)

    conn = sqlite3.connect(DATABASE_URL, check_same_thread=False)

    cursor = conn.cursor()

    loop = asyncio.get_event_loop()

    executor.start_polling(dp, on_startup=on_startup, skip_updates=True, loop=loop)

    create_table_query = """
    CREATE TABLE IF NOT EXISTS mute_list (
        user_id INTEGER PRIMARY KEY,
        mute_time TIMESTAMP,
        unmute_time TIMESTAMP,
        reason TEXT,
        admin INTEGER
    );
    """
    conn.execute(create_table_query)

    create_top_table = '''
    CREATE TABLE IF NOT EXISTS message_top (
        user_id INTEGER PRIMARY KEY,
        message_count INTEGER
    );
    '''
    conn.execute(create_top_table)

    create_admin_table = '''
    CREATE TABLE IF NOT EXISTS staff (
        user_id INTEGER PRIMARY KEY
    );
    '''
    conn.execute(create_admin_table)

    create_creators_table = '''
    CREATE TABLE IF NOT EXISTS creators (
        user_id INTEGER PRIMARY KEY
    );
    '''
    conn.execute(create_creators_table)

    create_giveawayban_table = '''
    CREATE TABLE IF NOT EXISTS giveawayban_list (
        user_id INTEGER PRIMARY KEY
    );
    '''
    conn.execute(create_giveawayban_table)

    create_giveaway_auto_table = '''
    CREATE TABLE IF NOT EXISTS giveaway_auto (
        user_id INTEGER PRIMARY KEY
    );
    '''
    conn.execute(create_giveaway_auto_table)

    create_giveaway_count_table = '''
    CREATE TABLE IF NOT EXISTS giveaway_count (
        user_id INTEGER PRIMARY KEY,
        gives_count INTEGER
    );
    '''
    conn.execute(create_giveaway_count_table)

    create_ludik_balance_table = '''
    CREATE TABLE IF NOT EXISTS ludik_balance (
        user_id INTEGER PRIMARY KEY,
        count INTEGER,
        wins INTEGER,
        allwins INTEGER,
        balance INTEGER,
        username TEXT
    );
    '''
    conn.execute(create_ludik_balance_table)

    create_cont = f"CREATE TABLE IF NOT EXISTS contests (giveaway_id INTEGER PRIMARY KEY, creator_id INTEGER, prizes TEXT, desc TEXT, end TIMESTAMP, users TEXT)"
    conn.execute(create_cont)
