from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext, filters

from data_base import db_funcs
from keyboards import admin_kb


class MakingRecordFSM(StatesGroup):  # машина состояний 1
    student_profcom_id = State()
    reason_for_help = State()
    making_record_approval = State()


async def recording_start(message: types.Message) -> None:
    """Начало диалога внесения записи о новом выделении матпомощи."""
    await MakingRecordFSM.student_profcom_id.set()
    await message.reply('Введите номер профкарты кандидата на мат помощь')


async def get_profcom_id(message: types.Message, state: FSMContext) -> None:
    """Ловим номер профкарты и записываем в словарь."""
    async with state.proxy() as data:
        data['profcom_id'] = message.text
    await MakingRecordFSM.next()
    await message.reply('Теперь введите причину', reply_markup=admin_kb.reasons_kb_admin)


async def get_help_reason(message: types.Message, state: FSMContext) -> None:
    """Ловим название причины."""
    async with state.proxy() as data:
        data['reason'] = message.text
    flag = await sqlite_db.mat_help_opportunity(data.get('profcom_id'), message)
    if flag == 999:
        await state.finish()
        return
    elif flag < 2:
        await MakingRecordFSM.next()
        await message.reply('Внести новую запись о назначении материальной помощи?',
                            reply_markup=admin_kb.approval_kb_admin)
    else:
        await message.reply('Студент уже получил мат помощь 2 раза в этом семестре',
                            reply_markup=admin_kb.starting_kb_admin)
        await state.finish()


async def making_record(message: types.Message, state: FSMContext) -> None:
    """Отлавливаем подтверждение и вносим изменения в БД."""
    if message.text == 'Да':
        await sqlite_db.sql_add_command(state)
        await message.reply('Запись внесена', reply_markup=admin_kb.starting_kb_admin)
    else:
        await message.reply('OK', reply_markup=admin_kb.starting_kb_admin)
    await state.finish()


def register_make_record_handlers(dp: Dispatcher) -> None:
    dp.register_message_handler(recording_start, text='Материальная помощь студентам', state=None)
    dp.register_message_handler(get_profcom_id, filters.Regexp(r'\b\d{2}-\d{4}\b'),
                                state=MakingRecordFSM.student_profcom_id)
    dp.register_message_handler(get_help_reason, state=MakingRecordFSM.reason_for_help)
    dp.register_message_handler(making_record, state=MakingRecordFSM.making_record_approval)
