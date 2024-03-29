import asyncpg
from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart
from datetime import datetime
from loader import dp, db, bot
from data.config import ADMINS
from keyboards.default.menu import asosiy


@dp.message_handler(CommandStart(), state="*")
async def bot_start(message: types.Message):
    try:
        user = await db.add_user(telegram_id=message.from_user.id,
                                 full_name=message.from_user.full_name,
                                 username=message.from_user.username)
        # ADMINGA xabar beramiz
        count = await db.count_users()
        msg = f"{user[1]} bazaga qo'shildi.\nBazada {count} ta foydalanuvchi bor."
        await bot.send_message(chat_id=ADMINS[0], text=msg)

    except asyncpg.exceptions.UniqueViolationError:
        user = await db.select_user(telegram_id=message.from_user.id)
    
    await message.answer(f"Xush kelibsiz {message.from_user.full_name}", reply_markup=asosiy)
