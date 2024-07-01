# пишем тг бота на asyncio и aiogram
# также реализую работу базой данных и датафреймами
# хочу добавить работу с API token metrics https://tokenmetrics.io/
import asyncio

from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import ParseMode
from aiogram.utils.markdown import hbold, hlink
from aiogram.utils.emoji import emojize
from aiogram.dispatcher import FSMContext
import pandas as pd
import sqlite3
import os
from dotenv import load_dotenv


load_dotenv()

bot = Bot(token=os.getenv("TOKEN"))
dp = Dispatcher(bot, storage=MemoryStorage())
