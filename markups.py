from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton

### select service
Two_GIS = InlineKeyboardButton(text = '2GIS', callback_data='2GIS')
Avito = InlineKeyboardButton(text = 'Avito', callback_data='Avito')
Youla = InlineKeyboardButton(text = 'Youla', callback_data='Youla')
select_service = InlineKeyboardMarkup(row_width=1).add(Two_GIS, Avito, Youla)
###

### back to main menu inline
go_Main = InlineKeyboardButton(text = 'В главное меню', callback_data='go_Main')
main_Menu = InlineKeyboardMarkup(row_width=1).add(go_Main)
###

### main menu keyboard
kgo_Main = KeyboardButton('Главное меню')
kmain_Menu = ReplyKeyboardMarkup(resize_keyboard=True).add(kgo_Main)
###