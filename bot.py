from aiogram.utils import executor
from bot_init import dp
from handlers import client, admin, other
from data_base.sqlite_db import sql_start


async def on_startup(_):
    print('Bot is now online')
    sql_start()


def start_bot():
    admin.register_handlers_admin(dp)
    client.register_handlers_client(dp)
    other.register_handlers_other(dp)
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup)


if __name__ == '__main__':
    start_bot()
