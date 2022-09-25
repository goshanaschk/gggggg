import os
from database.sql_operations import *
from dotenv import load_dotenv

load_dotenv()
db = Database('main.db')
BOT_TOKEN = str(os.getenv("BOT_TOKEN"))

admins = db.get_admins_id()
admins = [int(i) for i in admins]