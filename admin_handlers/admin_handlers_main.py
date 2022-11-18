from aiogram import Dispatcher

from admin_handlers.admin_other import register_other_handlers_admin
from admin_handlers.admin_states.student_info_state import register_stud_info_handlers
from admin_handlers.admin_states.make_record_state import register_make_record_handlers


def register_admin_handlers(dp: Dispatcher) -> None:
    handlers = (
        register_other_handlers_admin,
        register_stud_info_handlers,
        register_make_record_handlers,
    )
    for handler in handlers:
        handler(dp)
