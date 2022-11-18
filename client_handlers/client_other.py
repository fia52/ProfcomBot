from aiogram import types, Dispatcher

from bot_init import bot
from keyboards import client_kb


async def commands_start(message: types.message) -> None:
    """Отлавливаем команду старт и выводим клиентскую клавиатуру."""
    try:
        await bot.send_message(message.from_user.id, 'Добро пожаловать, бот профкома на связи!',
                               reply_markup=client_kb.starting_kb_client)
        await message.delete()
    except Exception:
        await message.reply('Общение с ботом происходит через лс, напишите ему:\nhttps://t.me/ProfUniversary_bot')


async def profcom_time_command(message: types.Message) -> None:
    await bot.send_message(message.from_user.id, 'Вс-Чт с 9:00 до 20:00, Пт-Сб с 10:00 до 23:00')


async def profcom_location_command(message: types.Message) -> None:
    await bot.send_message(message.from_user.id, '2 этаж, 203 кабинет')


def register_other_handlers_client(dp: Dispatcher) -> None:
    dp.register_message_handler(commands_start, commands=['start', 'help'])
    dp.register_message_handler(profcom_time_command, text=['Время приёма документов'])
    dp.register_message_handler(profcom_location_command, text=['Расположение профкома'])
