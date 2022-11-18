import sqlite3 as sq

from aiogram.dispatcher import FSMContext
from aiogram import types

from keyboards import client_kb, admin_kb


def sql_start() -> None:
    global base, cur
    base = sq.connect('profcom_base.db', timeout=10)
    cur = base.cursor()
    if base:
        print('Data base connected')


async def sql_add_command(state: FSMContext) -> None:
    async with state.proxy() as data:
        cur.execute(f'UPDATE student SET reason_for_help = ? WHERE profcom_id = ?', (data.get("reason"), data.get("profcom_id")))

        cur.execute(f'SELECT how_many_times FROM student WHERE profcom_id == ?', (data.get("profcom_id"),))
        times = (cur.fetchone())[0]

        cur.execute(f'UPDATE student SET how_many_times = ? WHERE profcom_id = ?', (times + 1, data.get("profcom_id")))
        base.commit()

        cur.close()


async def get_line(profcom_id: str, message: types.message) -> str:
        cur.execute(f'SELECT * FROM student WHERE profcom_id == ?', (profcom_id,))
        line = cur.fetchone()
        try:
            response = f'''
            ФИО: {line[3]}
номер студенческого билета: {line[0]}
номер профкарты: {line[1]}
причина мат помощи: {line[2]}
сколько раз уже получил: {line[4]}
'''
            return response
        except TypeError:
            await message.reply('Видимо, вы ошиблись номером профкарты', reply_markup=admin_kb.starting_kb_admin)
            return ''


async def mat_help_opportunity(profcom_id: str, message: types.message) -> int:
        cur.execute(f'SELECT how_many_times FROM student WHERE profcom_id == ?', (profcom_id,))
        try:
            times = cur.fetchone()[0]
            return times
        except TypeError:
            await message.reply('Видимо, вы ошиблись номером профкарты', reply_markup=admin_kb.starting_kb_admin)
            return 999


async def get_prof_id(university_id: str, message: types.message) -> str:
        cur.execute(f'SELECT profcom_id FROM student WHERE university_id == ?', (university_id,))
        try:
            profcom_id = cur.fetchone()[0]
            return profcom_id
        except TypeError:
            await message.reply('Видимо, вы ошиблись номером студенческого', reply_markup=client_kb.starting_kb_client)
            return ''
