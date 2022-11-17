from aiogram.types import ReplyKeyboardMarkup, KeyboardButton  # , ReplyKeyboardRemove

button1 = KeyboardButton('Время приёма документов')
button2 = KeyboardButton('Расположение профкома')
button3 = KeyboardButton('Узнать номер профсоюзной карты')
# button4 = KeyboardButton('Поделиться номером', request_contact=True)
# button5 = KeyboardButton('Поделиться местоположением', request_location=True)

starting_kb_client = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=False)  # замещает клавиатуру обычную той, что мы создаём

starting_kb_client.add(button1).add(button2).add(button3)
# .row(button4, button5)     # insert(b3) добавит кнопку сбоку, если есть достаточно места| row (b1, b2, b3) - всё в одну строку
