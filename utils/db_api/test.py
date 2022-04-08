import asyncio

from postgre_sql import Database


async def test():
    db = Database()
    await db.create()

    # print("Users jadvalini yaratamiz...")
    # await db.drop_users()
    # await db.create_table_users()
    # print("Yaratildi")

    print("Foydalanuvchilarni qo'shamiz")

    await db.add_user("bekzod", "bekodev", 123456789)
    await db.add_user("olim", "olim223", 12341123)
    await db.add_user("1", "1", 131231)
    await db.add_user("1", "1", 23324234)
    await db.add_user("John", "JohnDoe", 4388229)
    print("Qo'shildi")

    users = await db.select_all_users()
    print(f"Barcha foydalanuvchilar: {users}")

    user = await db.select_user(id=5)
    print(f"Foydalanuvchi: {user}")

if __name__ == '__main__':
    asyncio.run(test())