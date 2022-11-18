from aiogram.utils import executor

from bot_init import dp
from handlers_main import register_all_handlers


def start_bot():
    register_all_handlers(dp)
    executor.start_polling(dp, skip_updates=True)


if __name__ == '__main__':
    start_bot()
