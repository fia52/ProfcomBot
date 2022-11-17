from aiogram.utils import executor
from bot_init import dp
from data_base.sqlite_db import sql_start
from handlers.handlers_main import register_all_handlers


async def on_startup(_):
    print('Bot is now online')
    sql_start()


def start_bot():
    register_all_handlers(dp)
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup)


if __name__ == '__main__':
    start_bot()
