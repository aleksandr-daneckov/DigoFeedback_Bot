from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command
from aiogram.types import CallbackQuery

from handlers import channels
from handlers.users import admins
from keyboards.default import menu_close
from keyboards.inline.meger_post import post_callback
from loader import dp, bot
from states import Test
from states.poster import NewPost


@dp.message_handler(text="111")
async  def create_post(message: types.Message):

    await message.answer("Отправьте мне пост на публикацию", reply_markup=menu_close)
    await Test.Q7.set()
@dp.message_handler(state=Test.Q7)
async def enter_message(message: types.Message, state: FSMContext):
        await state.update_data(post1=message.text)
        await Test.Q8.set()
        
@dp.callback_query_handler(post_callback.filter(action="post"), state=NewPost.Confirm)
async def confirm_post(call: CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        text = data.get("text")
        mention = data.get("mention")
    await state.finish()
    await call.message.edit_reply_markup()
    await call.message.answer("Вы отправили пост на проверку")
    await bot.send_message(chat_id=5986362309, text=f"Пользователь {mention} хочет сделать пост:")
    await bot.send_message(chat_id=5986362309, text=text, parse_mode="HTML", reply_markup=confirmation_keybord)


@dp.callback_query_handler(post_callback.filter(action="cansel"), state=NewPost.Confirm)
async def cansel_post(call: CallbackQuery, state: FSMContext):
    await state.finish()
    await call.message.edit_reply_markup()
    await call.message.answer("Вы отклонили пост")

@dp.callback_query_handler(post_callback.filter(action="post"), user_id=admins)
async def approve_post(call: CallbackQuery):
       await call.answer("Вы одобрили пост", show_alert=True)
       target_channel = channels[0]
       message = await call.message.edit_reply_markup()
       await message.send_copy(chat_id=target_channel)

@dp.callback_query_handler(post_callback.filter(action="cancel"), user_id=admins)
async def decline_post(call: CallbackQuery):
        await call.answer("Вы отклонили этот пост.", show_alert=True)
        await call.message.edit_reply_markup()