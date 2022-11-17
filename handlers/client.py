from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext, filters
from aiogram.dispatcher.filters.state import State, StatesGroup

from bot_init import bot
from keyboards import client_kb
from data_base import sqlite_db


class FSMgetProfId(StatesGroup):
    profcom_id_giving = State()


async def commands_start(message: types.message) -> None:
    """Отлавливаем команду старт и выводим клиентскую клавиатуру."""
    try:
        await bot.send_message(message.from_user.id, 'Добро пожаловать, бот профкома на связи!',
                               reply_markup=client_kb.starting_kb_client)
        await message.delete()
    except Exception:
        await message.reply('Общение с ботом происходит через лс, напишите ему:\nhttps://t.me/ProfUniversary_bot')


async def student_info_load(message: types.Message) -> None:
    """Начало диалога предоставления информации о студенте."""
    await FSMgetProfId.profcom_id_giving.set()
    await message.reply('Введите номер студенческого билета')


async def prof_id_load(message: types.Message, state: FSMContext) -> None:
    """Получаем и выдаём информацию о профкарте студента по его студенческому."""
    profcom_id = await sqlite_db.get_prof_id(message.text, message)
    if profcom_id:
        response = f"Номер вашей профкарты: {profcom_id}"
        await message.reply(response, reply_markup=client_kb.starting_kb_client)
    await state.finish()


async def profcom_time_command(message: types.Message) -> None:
    await bot.send_message(message.from_user.id, 'Вс-Чт с 9:00 до 20:00, Пт-Сб с 10:00 до 23:00')


async def profcom_location_command(message: types.Message) -> None:
    await bot.send_message(message.from_user.id, '2 этаж, 203 кабинет')


def register_handlers_client(dp: Dispatcher) -> None:
    dp.register_message_handler(student_info_load, text='Узнать номер профсоюзной карты', state=None)
    dp.register_message_handler(prof_id_load, filters.Regexp(r'\b\d{2}-[А-Я]-\d{5}\b'),
                                state=FSMgetProfId.profcom_id_giving)
    dp.register_message_handler(commands_start, commands=['start', 'help'])
    dp.register_message_handler(profcom_time_command, text=['Время приёма документов'])
    dp.register_message_handler(profcom_location_command, text=['Расположение профкома'])
