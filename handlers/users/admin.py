import os
import asyncio
from aiogram import types
from data.config import ADMINS
from states.reklama import ADV
from loader import dp, db, bot
from datetime import datetime
from xlsxwriter.workbook import Workbook
from aiogram.dispatcher import FSMContext
from keyboards.inline.menu_inline import advertisement


@dp.message_handler(text="/reklama", user_id=ADMINS, state="*")
async def send_ad_to_all(message: types.Message):
    await message.answer("Reklama uchun rasm jo'nating")
    await ADV.image.set()


@dp.message_handler(content_types=['photo'], state=ADV.image, user_id=ADMINS)
async def get_image(message: types.Message, state: FSMContext):
    image = message.photo[-1].file_id

    await state.update_data(
        {'image': image}
    )
    await message.answer("Reklama matnini kiriting")
    await ADV.next()


@dp.message_handler(state=ADV.content, user_id=ADMINS)
async def get_text(message: types.Message, state: FSMContext):
    content = message.text

    if len(content) > 1020:
        await message.answer("Reklama matni 1000 belgidan ko'p bo'lmasligi lozim")
        await ADV.content.set()
    else:
        await state.update_data(
            {'content': content}
        )
        markup = await advertisement()
        await message.answer("Barcha ma'lumotlar to'g'rimi?", reply_markup=markup)
        await ADV.next()


@dp.callback_query_handler(text="no", state=ADV.confirm, user_id=ADMINS)
async def delete_adv(call: types.CallbackQuery, state: FSMContext):
    await call.message.answer("Barcha ma'lumotlar o'chirildi")
    await call.message.delete()
    await state.finish()


@dp.callback_query_handler(text="yes", state=ADV.confirm, user_id=ADMINS)
async def send_adv(call: types.CallbackQuery, state: FSMContext):
    await call.message.delete()
    data = await state.get_data()
    img = data.get('image')
    content = data.get('content')
    users = await db.select_all_users()
    for user in users[:2]:
        # print(user[3])
        try:
            user_id = user[3]
            await bot.send_photo(chat_id=user_id, photo=img, caption=content)
            await asyncio.sleep(0.05)
        except:
            continue
    await bot.send_message(chat_id=ADMINS[0], text="Reklama barchaga jo'natildi!")
    await state.finish()


@dp.message_handler(text="/author", user_id=ADMINS)
async def send_ad_to_all(message: types.Message):
    users = await db.select_all_users()
    for user in users[:2]:
        # print(user[3])
        try:
            user_id = user[3]
            await bot.send_message(chat_id=user_id, text="Talab va takliflar bo'lsa bog'lanishingiz mumkin 😎 @Bekzod_Rakhimov")
            await asyncio.sleep(0.05)
        except:
            continue
    await bot.send_message(chat_id=ADMINS[0], text="Reklama barchaga jo'natildi!")


@dp.message_handler(text="/allusers", user_id=ADMINS)
async def get_all_users(message: types.Message):
    users = await db.select_all_users()
    courses = await db.select_all_courses()
    teachers = await db.select_all_teachers()
    workbook = Workbook(
        f'data/{datetime.now().strftime("%Y_%m_%d")}.xlsx')  # Файл который надо передать админу
    worksheet = workbook.add_worksheet(name="Foydalanuvchilar")
    worksheet2 = workbook.add_worksheet(name="Kurslar")
    worksheet3 = workbook.add_worksheet(name="O'qituvchilar")

    for i, row in enumerate(users):
        for j, value in enumerate(row):
            worksheet.write(i, j, value)

    for i, row in enumerate(courses):
        for j, value in enumerate(row):
            worksheet2.write(i, j, value)

    for i, row in enumerate(teachers):
        for j, value in enumerate(row):
            worksheet3.write(i, j, value)
    workbook.close()

    await message.answer("Barcha ma'lumotlar faylga saqlandi")
    if os.path.exists(f'data/{datetime.now().strftime("%Y_%m_%d")}.xlsx'):
        await message.answer_document(
            open(f'data/{datetime.now().strftime("%Y_%m_%d")}.xlsx',
                 'rb'))
        os.remove(f'data/{datetime.now().strftime("%Y_%m_%d")}.xlsx')