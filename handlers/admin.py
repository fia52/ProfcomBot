from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext, filters
from aiogram.dispatcher.filters.state import State, StatesGroup
from bot_init import bot
from data_base import sqlite_db
from keyboards import admin_kb, client_kb

ID = None


class FSMadmin(StatesGroup):  # машина состояний1
    student_profcom_id = State()
    reason_for_help = State()
    making_record_approval = State()


class FSMgettingInfoByAdmin(StatesGroup):  # машина состояний2
    student_profcom_id = State()


async def admin_check(message: types.Message):
    global ID
    ID = message.from_user.id
    await bot.send_message(message.from_user.id, "Приветствую члена профкома!", reply_markup=admin_kb.starting_kb_admin)
    await message.delete()


async def get_student_info_start(message: types.Message):
    """Начало диалога предоставления информации о студенте."""
    if message.from_user.id == ID:
        await FSMgettingInfoByAdmin.student_profcom_id.set()
        await message.reply('Введите номер профкарты кандидата на мат помощь')


async def making_record_start(message: types.Message):
    """Начало диалога внесения записи о новом выделении матпомощи."""
    if message.from_user.id == ID:
        await FSMadmin.student_profcom_id.set()
        await message.reply('Введите номер профкарты кандидата на мат помощь')


async def cancel_handler(message: types.Message, state: FSMContext):
    """Выход из машины состояний."""
    current_state = await state.get_state()
    if current_state is None:
        return
    await state.finish()
    if message.from_user.id == ID:
        await message.reply('OK', reply_markup=admin_kb.starting_kb_admin)
    else:
        await message.reply('OK', reply_markup=client_kb.starting_kb_client)


async def get_info_by_prof_id(message: types.Message, state: FSMContext):
    try:
        response = sqlite_db.sql_get_line_command(message.text)
        print(response)
        await message.reply(response, reply_markup=admin_kb.starting_kb_admin)
    except:
        await message.reply('Видимо, вы ошиблись номером профкарты', reply_markup=admin_kb.starting_kb_admin)
    finally:
        await state.finish()


async def load_student_profcom_id(message: types.Message, state: FSMContext):
    """Ловим номер профкарты и записываем в словарь."""
    async with state.proxy() as data:
        data['profcom_id'] = message.text
    await FSMadmin.next()
    await message.reply('Теперь введите причину', reply_markup=admin_kb.reasons_kb_admin)


async def load_reason_for_help(message: types.Message, state: FSMContext):
    """Ловим название причины."""
    async with state.proxy() as data:
        data['reason'] = message.text
    try:
        flag = sqlite_db.opportunity_of_mat_help_bd(data.get('profcom_id'))
        if flag:
            await FSMadmin.next()
            await message.reply('Внести новую запись о назначении материальной помощи?',
                                reply_markup=admin_kb.approval_kb_admin)
        else:
            await message.reply('Студент уже получил мат помощь 2 раза в этом семестре',
                                reply_markup=admin_kb.starting_kb_admin)
            await state.finish()
    except:
        await message.reply('Видимо, вы ошиблись номером профкарты', reply_markup=admin_kb.starting_kb_admin)
        await state.finish()


async def making_record(message: types.Message, state: FSMContext):
    """Отлавливаем подтверждение и вносим изменения в БД."""
    if message.text == 'Да':
        await sqlite_db.sql_add_command(state)
        await message.reply('Запись внесена', reply_markup=admin_kb.starting_kb_admin)
    else:
        await message.reply('OK', reply_markup=admin_kb.starting_kb_admin)
    await state.finish()


def register_handlers_admin(dp: Dispatcher):
    dp.register_message_handler(get_student_info_start, text='Уточнить информацию о студенте', state=None)
    dp.register_message_handler(making_record_start, text='Материальная помощь студентам', state=None)
    dp.register_message_handler(cancel_handler, state="*", commands='отмена')
    dp.register_message_handler(cancel_handler, filters.Text(equals='отмена', ignore_case=True), state="*")
    dp.register_message_handler(get_info_by_prof_id, filters.Regexp(r'\b\d{2}-\d{4}\b'),
                                state=FSMgettingInfoByAdmin.student_profcom_id)
    dp.register_message_handler(load_student_profcom_id, filters.Regexp(r'\b\d{2}-\d{4}\b'),
                                state=FSMadmin.student_profcom_id)
    dp.register_message_handler(load_reason_for_help, state=FSMadmin.reason_for_help)
    dp.register_message_handler(making_record, state=FSMadmin.making_record_approval)
    dp.register_message_handler(admin_check, commands=['moderator'], is_chat_admin=True)
