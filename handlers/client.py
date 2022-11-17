from aiogram import types, Dispatcher
from bot_init import bot
from keyboards import client_kb
from aiogram.dispatcher import FSMContext, filters
from aiogram.dispatcher.filters.state import State, StatesGroup
from data_base import sqlite_db


class FSMgettingInfoByStudent(StatesGroup):  # машина состояний2
    profcom_id_giving = State()


async def get_student_info(message: types.Message):
    """Начало диалога предоставления информации о студенте."""
    await FSMgettingInfoByStudent.profcom_id_giving.set()
    await message.reply('Введите номер студенческого билета')


async def get_info_by_student_id(message: types.Message, state: FSMContext):
    """Получаем и выдаём информацию о профкарте студента по его студенческому."""
    try:
        response = sqlite_db.sql_get_prof_id_command(message.text)
        await message.reply(response, reply_markup=client_kb.starting_kb_client)
    except:
        await message.reply('Видимо, вы ошиблись номером студенческого', reply_markup=client_kb.starting_kb_client)
    finally:
        await state.finish()


async def commands_start(message: types.message):
    """Отлавливаем команду старт и выводим клиентскую клавиатуру."""
    try:
        await bot.send_message(message.from_user.id, 'Добро пожаловать, бот профкома на связи!',
                               reply_markup=client_kb.starting_kb_client)
        await message.delete()
    except:
        await message.reply('Общение с ботом происходит через лс, напишите ему:\nhttps://t.me/ProfUniversary_bot')


async def profcom_time_command(message: types.Message):
    await bot.send_message(message.from_user.id, 'Вс-Чт с 9:00 до 20:00, Пт-Сб с 10:00 до 23:00')


async def profcom_location_command(message: types.Message):
    await bot.send_message(message.from_user.id, '2 этаж, 203 кабинет')


def register_handlers_client(dp: Dispatcher):
    dp.register_message_handler(get_student_info, text='Узнать номер профсоюзной карты', state=None)
    dp.register_message_handler(get_info_by_student_id, filters.Regexp(r'\b\d{2}-[А-Я]-\d{5}\b'),
                                state=FSMgettingInfoByStudent.profcom_id_giving)
    dp.register_message_handler(commands_start, commands=['start', 'help'])
    dp.register_message_handler(profcom_time_command, text=['Время приёма документов'])
    dp.register_message_handler(profcom_location_command, text=['Расположение профкома'])
