import random
from data.config import *
import aiogram
import emoji
from main import bot
from aiogram import types
from main import dp
from keyboards.default import *
from keyboards.inline import *
from database.sql_operations import Database
from aiogram.utils.deep_linking import get_start_link
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from utils.misc import rate_limit

db = Database('main_db')



