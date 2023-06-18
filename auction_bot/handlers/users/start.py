from aiogram.dispatcher.filters.builtin import CommandStart
from aiogram import types
from keyboards.default import menu, menu_admin, menu_manager
from loader import dp, db, bot
from aiogram.dispatcher import FSMContext
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery
from keyboards.inline.callback_datas import proverka_callback
from states.conditions import Test
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton



@dp.message_handler(text="❌ Закрыть ❌")
async def get_food(message: types.message):


    admin = await db.check_admin(message.from_user.id)

    if admin:
        await message.answer("🗒 Меню бота", reply_markup=menu_admin)
    else:
        await message.answer("🗒 Меню бота", reply_markup=menu)



@dp.message_handler(text="❌ Закрыть ❌", state=(Test.Q1, Test.Q2, Test.Q3, Test.Q4, Test.Q5, Test.Q6, Test.Q7,
                                               Test.Q8, Test.Q9, Test.Q10, Test.Q11, Test.Q12, Test.Q13, Test.Q14,
                                               Test.Q15, Test.Q16, Test.Q17, Test.Q18, Test.Q19, Test.Q20, Test.Q21,
                                               Test.Q22, Test.Q23, Test.Q24, Test.Q25, Test.Q26, Test.Q27, Test.Q28,
                                               Test.Q29, Test.Q30))

async def get_food(message: types.message, state: FSMContext):
    admin = await db.check_admin(message.from_user.id)

    if admin:
        await message.answer("🗒 Меню бота", reply_markup=menu_admin)
    else:
        await message.answer("🗒 Меню бота", reply_markup=menu)

    await state.finish()





@dp.message_handler(CommandStart())
async def bot_start(message: types.Message, state: FSMContext):


    user = await db.select_username(message.from_user.id)


    if not user:

        if not message.from_user.username:
            proverka_keyboard = InlineKeyboardMarkup(inline_keyboard=[
                [
                    InlineKeyboardButton(text='📲 Зарегистрироваться', callback_data=proverka_callback.new(prefix="a"))
                ]
            ])
            await message.answer("⚠ Извините, но мы не можем Вас зарегистрировать, так как у Вас не заполнено имя пользователя (username) "
                                 "в настройках Telegram.\nЗаполните имя пользователя и нажмите на кнопку ниже", reply_markup=proverka_keyboard)

            await Test.Q1.set()

        else:

            phone_keyboard = ReplyKeyboardMarkup(resize_keyboard=True).add(KeyboardButton('📱 Подтвердить', request_contact=True))


            await message.answer(f"Уважаемый(ая) {message.from_user.first_name}!\nМы боремся со спамом и мошенниками! "
                                 f"Для минимизации Ваших рисков, пожалуйста подтвердите свой номер телефона!", reply_markup=phone_keyboard)

            await Test.Q2.set()

    else:

        admin = await db.check_admin(message.from_user.id)

        if admin:
            await message.answer("🗒 Меню бота", reply_markup=menu_admin)
        else:
            manager = await db.check_manager(message.from_user.id)
            if manager:
                await message.answer("🗒 Меню бота", reply_markup=menu_manager)
            else:
                await message.answer("🗒 Меню бота", reply_markup=menu)





@dp.callback_query_handler(proverka_callback.filter(), state=Test.Q1)
async def search_users(call: CallbackQuery, callback_data: dict, state: FSMContext):

    await call.answer(cache_time=60)
    await call.message.edit_reply_markup()

    if not call.from_user.username:
        proverka_keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [
                InlineKeyboardButton(text='📲 Зарегистрироваться', callback_data=proverka_callback.new(prefix="a"))
            ]
        ])
        await call.message.answer(
            "⚠ Извините, но мы не можем Вас зарегистрировать, так как у Вас не заполнено имя пользователя (username) "
            "в настройках Telegram.\nЗаполните имя пользователя и нажмите на кнопку ниже",
            reply_markup=proverka_keyboard)

        await Test.Q1.set()

    else:

        phone_keyboard = ReplyKeyboardMarkup(resize_keyboard=True).add(KeyboardButton('📱 Подтвердить', request_contact=True))

        await call.message.answer(f"Уважаемый(ая) {call.from_user.first_name}!\nМы боремся со спамом и мошенниками! "
                             f"Для минимизации Ваших рисков, пожалуйста подтвердите свой номер телефона!",
                             reply_markup=phone_keyboard)

        await Test.Q2.set()





@dp.message_handler(content_types=types.ContentTypes.CONTACT, state=Test.Q2)
async def bot_echo(message: types.Message, state: FSMContext):

    phone = message.contact.phone_number


    if message.from_user.id == message.contact.user_id:

        if phone[0:1] == "+":
            phone1 = phone[1:]

            await db.add_user(message.from_user.id,
                              message.from_user.username,
                              message.from_user.full_name,
                              phone1)




        else:

            await db.add_user(message.from_user.id,
                              message.from_user.username,
                              message.from_user.full_name,
                              phone)


        await message.answer("Добро пожаловать!", reply_markup=menu)

        await state.finish()

    else:

        number_request = ReplyKeyboardMarkup(resize_keyboard=True).add(KeyboardButton('📲 Зарегистрироваться', request_contact=True))
        await message.answer("⚠️ Вы прислали не свой номер телефона!", reply_markup=number_request)
        await Test.Q2.set()
































