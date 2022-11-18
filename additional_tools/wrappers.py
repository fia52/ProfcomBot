from aiogram import types
from config import admin_id_list


def admin_require(func):
    async def wrapper(message: types.Message):
        if message.from_user.id in admin_id_list:
            await func(message)

    return wrapper

