from aiogram.utils import executor
from bot_init import dp
from handlers import client, admin, other
from data_base.sqlite_db import sql_start


async def on_startup(_):
    print('Bot is now online')
    sql_start()

admin.register_handlers_admin(dp)
client.register_handlers_client(dp)

other.register_handlers_other(dp)  # порядок регистрации хендлеров важен

executor.start_polling(dp, skip_updates=True, on_startup=on_startup)  # 'skip_updates=True' - бот не будет отвечать на сообщения, которые пришли, пока он не был активен
