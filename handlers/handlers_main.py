from aiogram import Dispatcher

from handlers.admin import register_handlers_admin
from handlers.client import register_handlers_client
from handlers.other import register_handlers_other


def register_all_handlers(dp: Dispatcher) -> None:
    handlers = (
        register_handlers_admin,
        register_handlers_client,
        register_handlers_other,
    )
    for handler in handlers:
        handler(dp)
