from loader import dp, db, bot
from aiogram import types
from states.holatlar import DATA
from aiogram.dispatcher import FSMContext
from keyboards.inline.menu_inline import categories_keyboard, courses_keyboard, about_course, back, teachers_keyboard
from telegram_bot_pagination import InlineKeyboardPaginator
from aiogram.types import InlineKeyboardButton
from keyboards.default.menu import asosiy


@dp.message_handler(text="💻 Kompyuter kurslar", state="*")
async def get_cats(message: types.Message):
    markup = await categories_keyboard(type="comp")
    await message.answer("Bu yerda siz barcha kurslar haqida ma'lumot olishingiz mumkin", reply_markup=types.ReplyKeyboardRemove())
    await message.answer("Kerakli yo'nalishni tanlang", reply_markup=markup)
    await DATA.category.set()


@dp.message_handler(text="🗣 Ingliz tili (Beta)", state="*")
async def get_cats(message: types.Message):
    markup = await categories_keyboard(type="lang")
    await message.answer("Bu yerda siz barcha ingliz tili kurslari haqida ma'lumot olishingiz mumkin", reply_markup=types.ReplyKeyboardRemove())
    await message.answer("Kerakli yo'nalishni tanlang", reply_markup=markup)
    await DATA.category.set()


@dp.callback_query_handler(text="back", state=DATA.category)
async def get_course(call: types.CallbackQuery, state: FSMContext):
    await call.message.answer("Asosiy sahifa", reply_markup=asosiy)
    await call.message.delete()
    await state.finish()


@dp.callback_query_handler(state=DATA.category)
async def get_course(call: types.CallbackQuery, state: FSMContext):
    cat = call.data
    await state.update_data({
        'cat': cat
    })
    # print(cat)
    markup = await courses_keyboard(cat)
    if markup[1] > 0:
        await call.message.edit_text("Qaysi kurs haqida bilmoqchisiz?", reply_markup=markup[0])
        await DATA.next()
    else:
        await call.answer("Kurslar mavjud emas")


@dp.callback_query_handler(text="back", state=DATA.course)
async def get_course(call: types.CallbackQuery, state: FSMContext):
    cat = await state.get_data()
    category = cat.get('cat')
    data = await db.get_category_type(category)
    markup = await categories_keyboard(type=data[0]['type'])
    await call.message.edit_text("Kerakli yo'nalishni tanlang", reply_markup=markup)
    await DATA.category.set()


@dp.callback_query_handler(state=DATA.course)
async def all_info(call: types.CallbackQuery, state: FSMContext):
    course = call.data
    await state.update_data({
        'course': course
    })
    data = await db.get_course(course)
    markup = await about_course()
    # print(data)
    await call.message.answer_photo(photo=data['image_url'], caption=f"<b>► Kurs narxi: {data['price']} so'm/oyiga</b>\n\n{data['content']}", reply_markup=markup)
    await call.message.delete()
    await DATA.next()


@dp.callback_query_handler(text="back", state=DATA.about)
async def get_course(call: types.CallbackQuery, state: FSMContext):
    cat = await state.get_data()
    category = cat.get('cat')
    markup = await courses_keyboard(category)
    await call.message.answer("Qaysi kurs haqida bilmoqchisiz?", reply_markup=markup[0])
    await call.message.delete()
    await DATA.course.set()


@dp.callback_query_handler(text="faq", state=DATA.about)
async def get_faq(call: types.CallbackQuery, state: FSMContext):
    status = call.data
    await state.update_data({
        'status': status
    })
    kurs = await state.get_data()
    course_slug = kurs.get('course')
    data = await db.get_coure_id(course_slug)
    # print(data)
    course_id = data[0]['id']
    faqs = await db.get_faqs(course_id)
    if faqs:
        await send_faq_page(call.message, faqs)
        await call.message.delete()
        await DATA.next()
    else:
        await call.answer("Mavjud emas")
    # for faq in faqs:
    #     await call.message.answer(f"<b>{faq['question']}</b>\n\n{faq['answer']}")
    # markup = await back()
    # await call.message.answer(text=f"{data['faq']}", reply_markup=markup)
    


@dp.callback_query_handler(text="batafsil", state=DATA.about)
async def get_faq(call: types.CallbackQuery, state: FSMContext):
    status = call.data
    await state.update_data({
        'status': status
    })
    kurs = await state.get_data()
    course_slug = kurs.get('course')
    data = await db.get_coure_id(course_slug)
    # print(data)
    course_id = data[0]['id']
    subjects = await db.get_subjects(course_id)
    if subjects:
        await send_character_page(call.message, subjects)
        # for subject in subjects:
        #     await call.message.answer(f"<b>{subject['title']}</b>\n\n{subject['content']}")
        await call.message.delete()
        await DATA.next()
    else:
        await call.answer("Mavjud emas")


@dp.callback_query_handler(text="teachers", state=DATA.about)
async def get_teachers(call: types.CallbackQuery, state: FSMContext):
    kurs = await state.get_data()
    course_slug = kurs.get('course')
    markup = await teachers_keyboard(course_slug)
    if markup[1] > 0:
        await call.message.answer("Kurs o'qituvchilari haqida", reply_markup=markup[0])
        await call.message.delete()
        await DATA.next()
    else:
        await call.answer("Mavjud emas")


@dp.callback_query_handler(text_contains='character', state=DATA.teacher)
async def characters_page_callback(call: types.CallbackQuery, state: FSMContext):
    kurs = await state.get_data()
    course_slug = kurs.get('course')
    status = kurs.get('status')
    data = await db.get_coure_id(course_slug)
    # print(data)
    course_id = data[0]['id']
    subjects = await db.get_subjects(course_id)
    faqs = await db.get_faqs(course_id)
    # await call.message.answer(f"{call.data}")
    if status == "batafsil":
        page = int(call.data.split('#')[1])
        await bot.delete_message(
            call.message.chat.id,
            call.message.message_id
        )
        await send_character_page(call.message, subjects, page)
    elif status == "faq":
        page = int(call.data.split('#')[1])
        await bot.delete_message(
            call.message.chat.id,
            call.message.message_id
        )
        await send_faq_page(call.message, faqs, page)


@dp.callback_query_handler(text="back", state=DATA.teacher)
async def all_info(call: types.CallbackQuery, state: FSMContext):
    kurs = await state.get_data()
    course_slug = kurs.get('course')
    data = await db.get_course(course_slug)
    markup = await about_course()
    # print(data)
    await call.message.answer_photo(photo=data['image_url'], caption=f"<b>► Kurs narxi: {data['price']} so'm/oyiga</b>\n\n{data['content']}", reply_markup=markup)
    await call.message.delete()
    await DATA.about.set()


@dp.callback_query_handler(state=DATA.teacher)
async def get_about_teacher(call: types.CallbackQuery, state: FSMContext):
    callback = call.data
    # print(callback)
    kurs = await state.get_data()
    course_slug = kurs.get('course')
    print(course_slug)
    course = await db.get_coure_id(course_slug)
    course_id = course[0]['id']
    data = await db.about_teacher(course_id, str(callback))
    # print(data)
    data = data[0]
    markup = await back()
    await call.message.answer_photo(photo=data['image_url'], caption=f"<b>{data['name']}</b>\n\n{data['content']}", reply_markup=markup)
    await call.message.delete()
    await DATA.next()


@dp.callback_query_handler(text="back", state=DATA.about_teacher)
async def all_info(call: types.CallbackQuery, state: FSMContext):
    kurs = await state.get_data()
    course_slug = kurs.get('course')
    markup = await teachers_keyboard(course_slug)
    # print(data)
    await call.message.answer("Kurs o'qituvchilari haqida", reply_markup=markup[0])
    await call.message.delete()
    await DATA.teacher.set()


async def send_character_page(call, character_pages, page=1):
    paginator = InlineKeyboardPaginator(
        len(character_pages),
        current_page=page,
        data_pattern='character#{page}'
    )

    paginator.add_after(InlineKeyboardButton('⬅️ Orqaga', callback_data='back'))
    msg = f"<b>{character_pages[page-1]['title']}</b>" + "\n\n"
    msg += character_pages[page-1]['content']
    await bot.send_message(
        call.chat.id,
        msg,
        reply_markup=paginator.markup,
        # parse_mode='Markdown'
    )


async def send_faq_page(call, character_pages, page=1):
    paginator = InlineKeyboardPaginator(
        len(character_pages),
        current_page=page,
        data_pattern='character#{page}'
    )

    paginator.add_after(InlineKeyboardButton('⬅️ Orqaga', callback_data='back'))
    msg = f"<b>{character_pages[page-1]['question']}</b>" + "\n\n"
    msg += character_pages[page-1]['answer']
    await bot.send_message(
        call.chat.id,
        msg,
        reply_markup=paginator.markup,
        # parse_mode='Markdown'
    )