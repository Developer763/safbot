import logging
import asyncio
from aiogram import Bot, Dispatcher, types, F
from aiogram.enums import ParseMode
from aiogram.filters import Command
from aiogram.types import ChatPermissions

import os

TOKEN = os.getenv("BOT_TOKEN")

logging.basicConfig(level=logging.INFO)

bot = Bot(token=TOKEN, parse_mode=ParseMode.HTML)
dp = Dispatcher()

# Хранение админов в памяти (можно заменить на базу)
admins = set()

# Команды
@dp.message(Command("start"))
async def start(message: types.Message):
    await message.answer("Привет! Я модератор-бот. Доступные команды: /ban, /mute, /warn, /kick, /addadmin, /removeadmin, /admins")

@dp.message(Command("addadmin"))
async def add_admin(message: types.Message):
    if not message.reply_to_message:
        return await message.reply("Нужно ответить на сообщение пользователя.")
    user_id = message.reply_to_message.from_user.id
    admins.add(user_id)
    await message.reply(f"✅ Пользователь {user_id} добавлен в администраторы.")

@dp.message(Command("removeadmin"))
async def remove_admin(message: types.Message):
    if not message.reply_to_message:
        return await message.reply("Нужно ответить на сообщение пользователя.")
    user_id = message.reply_to_message.from_user.id
    admins.discard(user_id)
    await message.reply(f"❌ Пользователь {user_id} снят с администраторов.")

@dp.message(Command("admins"))
async def list_admins(message: types.Message):
    if not admins:
        await message.reply("Администраторов пока нет.")
    else:
        text = "👮 Список администраторов:" + "\n".join([str(uid) for uid in admins])
        await message.reply(text)

@dp.message(Command("ban"))
async def ban_user(message: types.Message):
    if message.from_user.id not in admins:
        return await message.reply("У вас нет прав.")
    if not message.reply_to_message:
        return await message.reply("Нужно ответить на сообщение пользователя.")
    user_id = message.reply_to_message.from_user.id
    await bot.ban_chat_member(message.chat.id, user_id)
    await message.reply(f"🚫 Пользователь {user_id} забанен.")

@dp.message(Command("kick"))
async def kick_user(message: types.Message):
    if message.from_user.id not in admins:
        return await message.reply("У вас нет прав.")
    if not message.reply_to_message:
        return await message.reply("Нужно ответить на сообщение пользователя.")
    user_id = message.reply_to_message.from_user.id
    await bot.ban_chat_member(message.chat.id, user_id)
    await bot.unban_chat_member(message.chat.id, user_id)
    await message.reply(f"👢 Пользователь {user_id} кикнут.")

@dp.message(Command("mute"))
async def mute_user(message: types.Message):
    if message.from_user.id not in admins:
        return await message.reply("У вас нет прав.")
    if not message.reply_to_message:
        return await message.reply("Нужно ответить на сообщение пользователя.")
    user_id = message.reply_to_message.from_user.id
    permissions = ChatPermissions(can_send_messages=False)
    await bot.restrict_chat_member(message.chat.id, user_id, permissions=permissions)
    await message.reply(f"🔇 Пользователь {user_id} замьючен.")

@dp.message(Command("warn"))
async def warn_user(message: types.Message):
    if message.from_user.id not in admins:
        return await message.reply("У вас нет прав.")
    if not message.reply_to_message:
        return await message.reply("Нужно ответить на сообщение пользователя.")
    user = message.reply_to_message.from_user
    await message.reply(f"⚠️ Предупреждение пользователю {user.full_name}")

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
