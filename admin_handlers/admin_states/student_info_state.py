from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext, filters

from additional_tools.wrappers import admin_require
from data_base import db_funcs
from keyboards import admin_kb


class GettingInfoFSM(StatesGroup):  # машина состояний 2
    student_profcom_id = State()


@admin_require
async def getting_info_start(message: types.Message) -> None:
    """Начало диалога предоставления информации о студенте."""
    await GettingInfoFSM.student_profcom_id.set()
    await message.reply('Введите номер профкарты кандидата на мат помощь')


async def info_with_id(message: types.Message, state: FSMContext) -> None:
    """Получаем и выдаём информацию о студенте по его проф карте."""
    response = await db_funcs.get_line(message.text, message)
    if response:
        await message.reply(response, reply_markup=admin_kb.starting_kb_admin)
    await state.finish()


def register_stud_info_handlers(dp: Dispatcher) -> None:
    dp.register_message_handler(getting_info_start, text='Уточнить информацию о студенте', state=None)
    dp.register_message_handler(info_with_id, filters.Regexp(r'\b\d{2}-\d{4}\b'),
                                state=GettingInfoFSM.student_profcom_id)
