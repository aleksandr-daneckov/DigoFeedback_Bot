from aiogram.dispatcher.filters.builtin import CommandStart
from aiogram import types
from keyboards.default import menu, menu_admin, menu_manager, menu_close
from loader import dp, db, bot
from aiogram.dispatcher import FSMContext
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery
from keyboards.inline.callback_datas import select_callback
from states.conditions import Test
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton








@dp.message_handler(text="Менеджеры")
async def get_food(message: types.message, state: FSMContext):


    select_kb = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text='✔️Добавить менеджера', callback_data=select_callback.new(prefix="add"))
        ],
        [
            InlineKeyboardButton(text='❌Удалить менеджера', callback_data=select_callback.new(prefix="delete"))
        ],
    ])

    await message.answer("🔧Настройки", reply_markup=select_kb)

    await Test.Q3.set()


@dp.callback_query_handler(select_callback.filter(), state=Test.Q3)
async def search_users(call: CallbackQuery, callback_data: dict, state: FSMContext):

    await call.answer(cache_time=60)
    await call.message.edit_reply_markup()

    prefix = callback_data.get("prefix")
    await state.update_data(prefix=prefix)


    await call.message.answer("👦Введите telegram id пользовтеля", reply_markup=menu_close)
    await Test.Q4.set()


@dp.message_handler(state=Test.Q4)
async def get_food(message: types.message, state: FSMContext):

    telegram_id_manager = message.text

    try:
        user = await db.select_username(telegram_id_manager)

        if user:
            data = await state.get_data()

            prefix = data.get("prefix")

            if prefix == "add":
                await db.update_manager(telegram_id_manager)
                await message.answer("✔️Добавлен новый менеджер", reply_markup=menu_admin)

            else:
                await db.update_manager_2(telegram_id_manager)
                await message.answer("❌Менеджер удален", reply_markup=menu_admin)
            await state.finish()

        else:
            await message.answer("🤷Пользователь с таким id отсутствует в базе", reply_markup=menu_close)

    except:
        await message.answer("❗️Ведите цифры!")




@dp.message_handler(text="Рассылка")
async def get_food(message: types.message, state: FSMContext):

    await message.answer("🧑‍💻Выберите обращение", reply_markup=menu_close)

    await Test.Q5.set()

@dp.message_handler(state=Test.Q5)
async def get_food(message: types.message, state: FSMContext):

    text = message.text


    all_tg = []


    all_users = await db.search_all_tg()

    for i in all_users:
        tg = i['telegram_id']
        all_tg.append(tg)


    for tlg in all_tg:
        await bot.send_message(chat_id=tlg, text=text)




    await message.answer("✉️ Обращение направлено менеджеру!")

    all_tg.clear()
    await state.finish()




























