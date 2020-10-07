from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.builtin import Command
from aiogram.types import ReplyKeyboardRemove
from aiogram.utils.markdown import hcode

from data.config import admins
from keyboards.default import contact_button, location_button
from loader import dp
from utils.db_api import quick_commands as commands


@dp.message_handler(Command("tel"))
async def bot_start(message: types.Message, state: FSMContext):
    await message.answer("Пришли мне свой номер телефона", reply_markup=contact_button.keyboard)
    await state.set_state("tel")


@dp.message_handler(state="tel", content_types=types.ContentType.CONTACT)
async def enter_email(message: types.Message, state: FSMContext):
    # contact = message.contact
    tel = message.contact
    # await message.answer(text=f"{tel.phone_number}, {tel.user_id}", reply_markup=ReplyKeyboardRemove())
    await commands.update_user_email(tel=tel.phone_number, id=message.from_user.id)
    user = await commands.select_user(id=message.from_user.id)
    await message.answer("Данные обновлены. Запись в БД: \n" +
                         hcode(f"id={user.id}\n"
                               f"name={user.name}\n"
                               f"tel={user.tel}"), reply_markup=ReplyKeyboardRemove())
    await dp.bot.send_message("54309418", "В базу добавлен новый ползователь: \n" +
                              hcode(f"id={user.id}\n"
                                    f"name={user.name}\n"
                                    f"tel={user.tel}"))
    await state.finish()


@dp.message_handler(Command("send_location"))
async def get_location(message: types.Message, state: FSMContext):
    await message.answer(f"Press button below to send your location", reply_markup=location_button.keyboard)
    await state.set_state("location")


@dp.message_handler(state="location", content_types=types.ContentType.LOCATION)
async def location_data(message: types.Message, state: FSMContext):
    location = message.location
    latitude = location.latitude
    longitude = location.longitude
    user = await commands.select_user(id=message.from_user.id)

    await message.answer(f"Спасибо. \n"
                         f"Latitude = {latitude}\n"
                         f"Longitude = {longitude}\n\n", reply_markup=ReplyKeyboardRemove())

    await dp.bot.send_message("54309418", "Посутпил новый заказ от: \n" +
                              hcode(f"id={user.id}\n"
                                    f"name={user.name}\n"
                                    f"tel={user.tel}"))

    await dp.bot.send_location("54309418", latitude=latitude, longitude=longitude)

    await state.finish()
