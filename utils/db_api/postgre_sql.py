from typing import Union

import asyncpg
from asyncpg import Connection
from asyncpg.pool import Pool

from data import config


class Database:
    def __init__(self):
        self.pool: Union[Pool, None] = None

    async def create(self):
        self.pool = await asyncpg.create_pool(
            user=config.DB_USER,
            password=config.DB_PASS,
            host=config.DB_HOST,
            database=config.DB_NAME,
        )

    async def execute(
            self,
            command,
            *args,
            fetch: bool = False,
            fetchval: bool = False,
            fetchrow: bool = False,
            execute: bool = False,
    ):
        async with self.pool.acquire() as connection:
            connection: Connection
            async with connection.transaction():
                if fetch:
                    result = await connection.fetch(command, *args)
                elif fetchval:
                    result = await connection.fetchval(command, *args)
                elif fetchrow:
                    result = await connection.fetchrow(command, *args)
                elif execute:
                    result = await connection.execute(command, *args)
            return result


    @staticmethod
    def format_args(sql, parameters: dict):
        sql += " AND ".join(
            [f"{item} = ${num}" for num, item in enumerate(parameters.keys(), start=1)]
        )
        return sql, tuple(parameters.values())

    async def add_user(self, full_name, username, telegram_id):
        sql = "INSERT INTO main_user (full_name, username, telegram_id) VALUES($1, $2, $3) returning *"
        return await self.execute(sql, full_name, username, telegram_id, fetchrow=True)

    async def select_all_users(self):
        sql = "SELECT * FROM main_user"
        return await self.execute(sql, fetch=True)

    async def select_all_courses(self):
        sql = "SELECT * FROM main_course"
        return await self.execute(sql, fetch=True)

    async def select_all_teachers(self):
        sql = "SELECT * FROM main_teacher"
        return await self.execute(sql, fetch=True)

    async def select_user(self, **kwargs):
        sql = "SELECT * FROM main_user WHERE "
        sql, parameters = self.format_args(sql, parameters=kwargs)
        return await self.execute(sql, *parameters, fetchrow=True)

    async def count_users(self):
        sql = "SELECT COUNT(*) FROM main_user"
        return await self.execute(sql, fetchval=True)

    async def update_user_username(self, username, telegram_id):
        sql = "UPDATE main_user SET username=$1 WHERE telegram_id=$2"
        return await self.execute(sql, username, telegram_id, execute=True)

    async def delete_users(self):
        await self.execute("DELETE FROM main_user WHERE TRUE", execute=True)

    async def drop_users(self):
        await self.execute("DROP TABLE main_user", execute=True)

    async def get_categories(self, type):
        sql = f"SELECT DISTINCT id, name, slug FROM main_category WHERE type='{type}'"
        return await self.execute(sql, fetch=True)

    async def get_category_type(self, slug):
        sql = f"SELECT DISTINCT type FROM main_category WHERE slug='{slug}'"
        return await self.execute(sql, fetch=True)
    
    async def get_category_id(self, slug):
        sql = f"SELECT DISTINCT id FROM main_category WHERE slug='{slug}'"
        return await self.execute(sql, fetch=True)

    async def get_coure_id(self, slug):
        sql = f"SELECT DISTINCT id FROM main_course WHERE slug='{slug}'"
        return await self.execute(sql, fetch=True)

    async def get_courses(self, category_id):
        sql = f"SELECT DISTINCT name, slug FROM main_course WHERE category_id={category_id}"
        return await self.execute(sql, fetch=True)

    async def get_teachers(self, course_id):
        sql = f"SELECT DISTINCT id, name, slug FROM main_teacher WHERE course_id={course_id}"
        return await self.execute(sql, fetch=True)

    async def about_teacher(self, course_id, slug):
        sql = f"SELECT DISTINCT * FROM main_teacher WHERE course_id={course_id} AND slug='{slug}'"
        return await self.execute(sql, fetch=True)

    async def count_courses(self, category_id):
        sql = f"SELECT COUNT(*) FROM main_course WHERE category_id={category_id}"
        return await self.execute(sql, fetchval=True)

    async def get_subjects(self, course_id):
        sql = f"SELECT DISTINCT * FROM main_subject WHERE course_id={course_id}"
        return await self.execute(sql, fetch=True)

    async def get_course(self, course_slug):
        sql = f"SELECT * FROM main_course WHERE slug='{course_slug}'"
        return await self.execute(sql, fetchrow=True)

    async def get_faqs(self, course_id):
        sql = f"SELECT DISTINCT * FROM main_faq WHERE course_id={course_id}"
        return await self.execute(sql, fetch=True)
