import logging

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData

from loader import db


# Kategoriyalar uchun keyboardyasab olamiz
async def categories_keyboard(type):
    # Keyboard yaratamiz
    markup = InlineKeyboardMarkup(row_width=1)

    # Bazadagi barcha kategoriyalarni olamiz
    categories = await db.get_categories(type)
    # Har bir kategoriya uchun quyidagilarni bajaramiz:
    for category in categories:
        # Kategoriyaga tegishli mahsulotlar sonini topamiz
        number_of_items = await db.count_courses(category["id"])

        if number_of_items > 0:
            # Tugma matnini yasab olamiz
            button_text = f"{category['name']} ({number_of_items} kurs)"
        else:
            # Tugma matnini yasab olamiz
            button_text = f"{category['name']}"

        # Tugma bosganda qaytuvchi callbackni yasaymiz: Keyingi bosqich +1 va kategoriyalar
        callback_data = category['slug']
        print(callback_data)
        # Tugmani keyboardga qo'shamiz
        markup.insert(
            InlineKeyboardButton(text=button_text, callback_data=callback_data)
        )
    markup.insert(InlineKeyboardButton(text="⬅️ Orqaga", callback_data="back"))
    # Keyboardni qaytaramiz
    return markup


# Kategoriyalar uchun keyboardyasab olamiz
async def courses_keyboard(category_slug):
    data = await db.get_category_id(category_slug)
    # print(data[0])
    category_id = data[0]['id']
    # Keyboard yaratamiz
    markup = InlineKeyboardMarkup(row_width=1)

    # Bazadagi barcha kategoriyalarni olamiz
    courses = await db.get_courses(category_id)
    # print(courses)
    # Har bir kategoriya uchun quyidagilarni bajaramiz:
    for course in courses:
        # Kategoriyaga tegishli mahsulotlar sonini topamiz
        # number_of_items = await db.count_products(category["id"])

        # Tugma matnini yasab olamiz
        button_text = f"{course['name']}"
    

        # Tugma bosganda qaytuvchi callbackni yasaymiz: Keyingi bosqich +1 va kategoriyalar
        callback_data = course['slug']
        print(callback_data)
        # Tugmani keyboardga qo'shamiz
        markup.insert(
            InlineKeyboardButton(text=button_text, callback_data=callback_data)
        )
    markup.insert(InlineKeyboardButton(text="⬅️ Orqaga", callback_data="back"))
    # Keyboardni qaytaramiz
    return markup, len(courses)


async def about_course():
    # Keyboard yaratamiz
    markup = InlineKeyboardMarkup(row_width=1)
    markup.insert(InlineKeyboardButton(text="👨‍🏫 O'qituvchilar", callback_data="teachers"))
    markup.insert(InlineKeyboardButton(text="📚 Mavzular ro'yhati", callback_data="batafsil"))
    markup.insert(InlineKeyboardButton(text="❓ Ko'p beriladigan savollar", callback_data="faq"))
    markup.insert(InlineKeyboardButton(text="⬅️ Orqaga", callback_data="back"))
    # Keyboardni qaytaramiz
    return markup

async def back():
    # Keyboard yaratamiz
    markup = InlineKeyboardMarkup(row_width=1)
    markup.insert(InlineKeyboardButton(text="⬅️ Orqaga", callback_data="back"))
    # Keyboardni qaytaramiz
    return markup


async def teachers_keyboard(course_slug):
    data = await db.get_coure_id(course_slug)
    # print(data)
    course_id = data[0]['id']
    # Keyboard yaratamiz
    markup = InlineKeyboardMarkup(row_width=1)

    # Bazadagi barcha kategoriyalarni olamiz
    teachers = await db.get_teachers(course_id)
    all_teachers = len(teachers)
    # Har bir kategoriya uchun quyidagilarni bajaramiz:
    for teacher in teachers:
        # Kategoriyaga tegishli mahsulotlar sonini topamiz
        # number_of_items = await db.count_products(category["id"])

        # Tugma matnini yasab olamiz
        button_text = f"{teacher['name']}"
    

        # Tugma bosganda qaytuvchi callbackni yasaymiz: Keyingi bosqich +1 va kategoriyalar
        callback_data = f'{teacher["slug"]}'
        print(callback_data)
        # Tugmani keyboardga qo'shamiz
        markup.insert(
            InlineKeyboardButton(text=button_text, callback_data=callback_data)
        )
    markup.insert(InlineKeyboardButton(text="⬅️ Orqaga", callback_data="back"))
    # Keyboardni qaytaramiz
    return markup, all_teachers


async def advertisement():
    markup = InlineKeyboardMarkup(row_width=2)
    markup.insert(InlineKeyboardButton(text="✅ Ha", callback_data="yes"))
    markup.insert(InlineKeyboardButton(text="❌ Yo'q", callback_data="no"))
    return markup