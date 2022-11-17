from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

button_mat_help = KeyboardButton('Материальная помощь студентам')
button_get_info = KeyboardButton('Уточнить информацию о студенте')

button1 = KeyboardButton('Проживание в общежитии')
button2 = KeyboardButton('Многодетная семья')
button3 = KeyboardButton('Неполная семья')
button4 = KeyboardButton('Инвалидность')

button_yes = KeyboardButton('Да')
button_no = KeyboardButton('Нет')

starting_kb_admin = ReplyKeyboardMarkup(resize_keyboard=True)
reasons_kb_admin = ReplyKeyboardMarkup(resize_keyboard=True)
approval_kb_admin = ReplyKeyboardMarkup(resize_keyboard=True)

starting_kb_admin.add(button_mat_help).add(button_get_info)
reasons_kb_admin.add(button1).insert(button2).add(button3).insert(button4)
approval_kb_admin.add(button_yes).add(button_no)
