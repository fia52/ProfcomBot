import json
import string

from aiogram import types, Dispatcher


async def cenz_checker(message: types.message) -> None:
    if {i.lower().translate(str.maketrans('', '', string.punctuation)) for i in message.text.split(' ')} \
            .intersection(set(json.load(open('cenz_controller/cenz_controller.json')))) != set():
        await message.reply('Выражайся культурнее')
        await message.delete()


def register_handlers_other(dp: Dispatcher) -> None:
    dp.register_message_handler(cenz_checker)
