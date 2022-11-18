from aiogram import Dispatcher

from admin_handlers.admin_handlers_main import register_admin_handlers
from client_handlers.client_handlers_main import register_client_handlers
from other_handlers.other import register_handlers_other


def register_all_handlers(dp: Dispatcher) -> None:
    handlers = (
        register_admin_handlers,
        register_client_handlers,
        register_handlers_other,
    )
    for handler in handlers:
        handler(dp)
