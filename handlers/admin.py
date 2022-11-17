from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext, filters
from aiogram.dispatcher.filters.state import State, StatesGroup

from bot_init import bot
from data_base import sqlite_db
from keyboards import admin_kb, client_kb

ID = None


class MakingRecordFSM(StatesGroup):  # машина состояний 1
    student_profcom_id = State()
    reason_for_help = State()
    making_record_approval = State()


class GettingInfoFSM(StatesGroup):  # машина состояний 2
    student_profcom_id = State()


async def admin_check(message: types.Message) -> None:
    """Отлавливаем лишь сообщение от админа группы, выводим клавиатуру админа."""
    global ID
    ID = message.from_user.id
    await bot.send_message(message.from_user.id, "Приветствую члена профкома!", reply_markup=admin_kb.starting_kb_admin)
    await message.delete()


async def getting_info_start(message: types.Message) -> None:
    """Начало диалога предоставления информации о студенте."""
    if message.from_user.id == ID:
        await GettingInfoFSM.student_profcom_id.set()
        await message.reply('Введите номер профкарты кандидата на мат помощь')


async def recording_start(message: types.Message) -> None:
    """Начало диалога внесения записи о новом выделении матпомощи."""
    if message.from_user.id == ID:
        await MakingRecordFSM.student_profcom_id.set()
        await message.reply('Введите номер профкарты кандидата на мат помощь')


async def cancel_handler(message: types.Message, state: FSMContext) -> None:
    """Выход из машины состояний."""
    current_state = await state.get_state()
    if current_state is None:
        return
    await state.finish()
    if message.from_user.id == ID:
        await message.reply('OK', reply_markup=admin_kb.starting_kb_admin)
    else:
        await message.reply('OK', reply_markup=client_kb.starting_kb_client)


async def info_with_id(message: types.Message, state: FSMContext) -> None:
    """Получаем и выдаём информацию о студенте по его проф карте."""
    response = await sqlite_db.get_line(message.text, message)
    if response:
        await message.reply(response, reply_markup=admin_kb.starting_kb_admin)
    await state.finish()


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


def register_handlers_admin(dp: Dispatcher) -> None:
    dp.register_message_handler(getting_info_start, text='Уточнить информацию о студенте', state=None)
    dp.register_message_handler(recording_start, text='Материальная помощь студентам', state=None)
    dp.register_message_handler(cancel_handler, state="*", commands='отмена')
    dp.register_message_handler(cancel_handler, filters.Text(equals='отмена', ignore_case=True), state="*")
    dp.register_message_handler(info_with_id, filters.Regexp(r'\b\d{2}-\d{4}\b'),
                                state=GettingInfoFSM.student_profcom_id)
    dp.register_message_handler(get_profcom_id, filters.Regexp(r'\b\d{2}-\d{4}\b'),
                                state=MakingRecordFSM.student_profcom_id)
    dp.register_message_handler(get_help_reason, state=MakingRecordFSM.reason_for_help)
    dp.register_message_handler(making_record, state=MakingRecordFSM.making_record_approval)
    dp.register_message_handler(admin_check, commands=['moderator'], is_chat_admin=True)
