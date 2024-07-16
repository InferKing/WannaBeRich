# реализовываю бота в телеграмм для анализа доходов и расходов пользователя
# что он по факту должен уметь
# минимум:
# - получать информацию от пользователя о доходах и расходах
# - показывать информацию о доходах и расходах за некоторый период
# - предоставлять выбор категорий трат пользователя для дальнейшего анализа
# - устанавливать начальный баланс на карте пользователя
# дополнительно:
# - оповещения пользователя о выполненных расходах
# - настройка оповещений о расходах (насколько часто оповещает) 
# - каждый пользователь сам настраивает категории (добавляет, удаляет, изменяет)
# - у пользователя может быть несколько карт, соответственно, пользователю нужно давать возможность 
# добавлять карты и их счет, а также удалять их и изменять. 

import asyncio

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
import logging
import pandas as pd
import sqlite3
import os
from dotenv import load_dotenv
from config import ConfigSelector

app_config = ConfigSelector.get_config(level=logging.DEBUG)
logging.basicConfig(level=app_config.CONFIG_LEVEL)

async def main():
    load_dotenv()
    bot = Bot(token=os.getenv("BOT_TOKEN"))
    dp = Dispatcher()
    dp.include_router(question_router)
    dp.include_router(not_registered_router)
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    from handlers.questions import router as question_router
    from handlers.not_registered import router as not_registered_router
    asyncio.run(main())