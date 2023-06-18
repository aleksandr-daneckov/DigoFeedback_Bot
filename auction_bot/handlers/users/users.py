from aiogram.dispatcher.filters.builtin import CommandStart
from aiogram import types
from keyboards.default import menu, menu_admin, menu_manager, menu_close
from loader import dp, db, bot
from aiogram.dispatcher import FSMContext
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery
from keyboards.inline.callback_datas import proverka_callback
from states.conditions import Test
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton



@dp.message_handler(text="Обращение")
async def appeals(message: types.message, FSMContext):
    await message.answer("Ведите текст сообщения", reply_markup=menu_close)

    await Test.Q6.set()

@dp.message_handler(state=Test.Q6)
async def get_food(message: types.message, state: FSMContext):

    text = message.text





