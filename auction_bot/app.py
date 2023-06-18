import logging

from aiogram import executor

from loader import dp, db, scheduler
import middlewares, filters, handlers
from utils.notify_admins import on_startup_notify

from aiogram_dialog import DialogRegistry

# from handlers.users.my_auctions import auction_dialog





# async def min_minute():
#     scheduler.add_job(minus_minute, "interval", seconds=60)





async def on_startup(dispatcher):

    logging.info("Создаем подключение к базе данных")
    await db.create()


    logging.info("Готово.")

    await on_startup_notify(dispatcher)

    # await min_minute()

    registry = DialogRegistry(dispatcher)

    # registry.register(auction_dialog)




    # scheduler_run1()

if __name__ == '__main__':
    scheduler.start()
    executor.start_polling(dp, on_startup=on_startup)
