from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext, filters
from aiogram.dispatcher.filters.state import State, StatesGroup

from keyboards import client_kb
from data_base import db_funcs


class FSMgetProfId(StatesGroup):
    profcom_id_giving = State()


async def student_info_load(message: types.Message) -> None:
    """Начало диалога предоставления информации о студенте."""
    await FSMgetProfId.profcom_id_giving.set()
    await message.reply('Введите номер студенческого билета')


async def prof_id_load(message: types.Message, state: FSMContext) -> None:
    """Получаем и выдаём информацию о профкарте студента по его студенческому."""
    profcom_id = await db_funcs.get_prof_id(message.text, message)
    if profcom_id:
        response = f"Номер вашей профкарты: {profcom_id}"
        await message.reply(response, reply_markup=client_kb.starting_kb_client)
    await state.finish()


def register_get_profid_handlers(dp: Dispatcher) -> None:
    dp.register_message_handler(student_info_load, text='Узнать номер профсоюзной карты', state=None)
    dp.register_message_handler(prof_id_load, filters.Regexp(r'\b\d{2}-[А-Я]-\d{5}\b'),
                                state=FSMgetProfId.profcom_id_giving)
