from aiogram import types, Dispatcher
import json, string


async def cenz_checker(message: types.message):
    if {i.lower().translate(str.maketrans('', '', string.punctuation)) for i in message.text.split(' ')} \
            .intersection(set(json.load(open('cenz/cenz.json')))) != set():
        await message.reply('Выражайся культурнее')
        await message.delete()


def register_handlers_other(dp: Dispatcher):
    dp.register_message_handler(cenz_checker)
