from aiogram import Dispatcher

from client_handlers.client_states.get_profid_state import register_get_profid_handlers
from client_handlers.client_other import register_other_handlers_client


def register_client_handlers(dp: Dispatcher) -> None:
    handlers = (
        register_get_profid_handlers,
        register_other_handlers_client,
    )
    for handler in handlers:
        handler(dp)
