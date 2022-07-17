import logging
from aiogram import Bot, Dispatcher, executor, types
from bs4 import BeautifulSoup as bs

import config as cfg
import markups as nav
import parsing as p

logging.basicConfig(level=logging.INFO)

bot = Bot(cfg.TOKEN)
dp = Dispatcher(bot)

gis_request, avito_request, youla_request = False, False, False

@dp.message_handler(commands=['start'])
async def start(message:types.Message):
    if message.chat.type == 'private':
        await bot.send_message(message.chat.id, "Привет👋", reply_markup=nav.kmain_Menu)
        await bot.send_message(message.chat.id, 'Выбери сервис ниже.', reply_markup=nav.select_service)

@dp.message_handler()
async def bot_message(message:types.Message):
    if message.chat.type == 'private':
        global gis_request, avito_request, youla_request

        if message.text == 'Главное меню':
            await bot.send_message(message.chat.id, 'Выбери сервис ниже.', reply_markup=nav.select_service)

        if gis_request:
            gis_request = False
            request_msg = message.text

            msg = await bot.send_message(message.chat.id, "Ожидайте...")
            request_msg = p.p2gis(request_msg)

            await bot.delete_message(message.chat.id, msg.message_id)
            await bot.send_message(message.chat.id, "Готово!")
            await message.reply_document(open(f'2gis/{request_msg}.xlsx', 'rb'), reply_markup=nav.main_Menu)

        if avito_request:
            avito_request = False
            request_msg = message.text

            msg = await bot.send_message(message.chat.id, "Ожидайте...")
            request_msg = p.pAvito(request_msg)

            await bot.delete_message(message.chat.id, msg.message_id)
            await bot.send_message(message.chat.id, "Готово!")
            await message.reply_document(open(f'avito/{request_msg}.xlsx', 'rb'), reply_markup=nav.main_Menu)

        if youla_request:
            youla_request = False
            request_msg = message.text

            msg = await bot.send_message(message.chat.id, "Ожидайте...")
            request_msg = p.pYoula(request_msg)

@dp.callback_query_handler(text='2GIS')
async def Two_GIS(callback: types.CallbackQuery):
    global gis_request
    gis_request = True
    await bot.delete_message(callback.from_user.id, callback.message.message_id)
    await bot.send_message(callback.from_user.id, "📄 Введите запрос\n📄 (запрос/город)", reply_markup=nav.main_Menu)

@dp.callback_query_handler(text='Avito')
async def Avito(callback: types.CallbackQuery):
    global avito_request
    avito_request = True
    await bot.delete_message(callback.from_user.id, callback.message.message_id)
    await bot.send_message(callback.from_user.id, "📄 Введите запрос\n📄 (запрос/город)", reply_markup=nav.main_Menu)

@dp.callback_query_handler(text='Youla')
async def Youla(callback: types.CallbackQuery):
    global youla_request
    youla_request = True
    await bot.delete_message(callback.from_user.id, callback.message.message_id)
    await bot.send_message(callback.from_user.id, "📄 Введите запрос\n📄 (запрос/город)", reply_markup=nav.main_Menu)


@dp.callback_query_handler(text="go_Main")
async def go_Main(callback: types.CallbackQuery):
    global gis_request, avito_request, youla_request
    gis_request, avito_request, youla_request = False, False, False
    await bot.delete_message(callback.from_user.id, callback.message.message_id)
    await bot.send_message(callback.from_user.id,
"""Привет👋
Выбери нужный сервис ниже.""", reply_markup=nav.select_service)

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates = True) 