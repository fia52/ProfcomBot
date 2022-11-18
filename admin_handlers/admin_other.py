from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext, filters

from bot_init import bot
from keyboards import admin_kb, client_kb


async def admin_check(message: types.Message) -> None:
    """Отлавливаем лишь сообщение от админа группы, выводим клавиатуру админа."""
    await bot.send_message(message.from_user.id, "Приветствую члена профкома!", reply_markup=admin_kb.starting_kb_admin)
    await message.delete()


async def cancel_handler(message: types.Message, state: FSMContext) -> None:
    """Выход из машины состояний."""
    current_state = await state.get_state()
    if current_state is None:
        return
    await state.finish()
    await message.reply('OK', reply_markup=admin_kb.starting_kb_admin)
    # else:
    #     await message.reply('OK', reply_markup=client_kb.starting_kb_client)


def register_other_handlers_admin(dp: Dispatcher) -> None:
    dp.register_message_handler(cancel_handler, filters.Text(equals='отмена', ignore_case=True), state="*")
    dp.register_message_handler(admin_check, commands=['moderator'], is_chat_admin=True)
