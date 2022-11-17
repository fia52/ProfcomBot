import sqlite3 as sq


def sql_start():
    global base, cur
    base = sq.connect('profcom_base.db', timeout=10)
    cur = base.cursor()
    if base:
        print('Data base connected')


async def sql_add_command(state):
    async with state.proxy() as data:
        params1 = (data.get("reason"), data.get("profcom_id"))
        cur.execute(f'UPDATE student SET reason_for_help = ? WHERE profcom_id = ?', params1)

        params2 = (data.get("profcom_id"),)
        cur.execute(f'SELECT how_many_times FROM student WHERE profcom_id == ?', params2)
        times = (cur.fetchone())[0]

        params3 = (times + 1, data.get("profcom_id"))
        cur.execute(f'UPDATE student SET how_many_times = ? WHERE profcom_id = ?', params3)
        base.commit()


def sql_get_line_command(profcom_id: str) -> str:
    params = (profcom_id,)
    cur.execute(f'SELECT * FROM student WHERE profcom_id == ?', params)
    line = cur.fetchone()
    response = f'''
    ФИО: {line[3]}
номер студенческого билета: {line[0]}
номер профкарты: {line[1]}
причина мат помощи: {line[2]}
сколько раз уже получил: {line[4]}
'''
    return response


def opportunity_of_mat_help_bd(profcom_id: str) -> bool:
    params = (profcom_id,)
    cur.execute(f'SELECT how_many_times FROM student WHERE profcom_id == ?', params)
    times = (cur.fetchone())[0]
    return times < 2


def sql_get_prof_id_command(university_id):
    params = (university_id,)
    cur.execute(f'SELECT profcom_id FROM student WHERE university_id == ?', params)
    profcom_id = (cur.fetchone())[0]
    response = f"Номер вашей профкарты: {profcom_id}"
    return response
