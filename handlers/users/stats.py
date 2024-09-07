from aiogram.types import Message
from loader import dp,bot,db,ADMINS
from aiogram.filters import Command
from menucommands.set_bot_commands  import set_default_commands
import logging
import sqlite3
from datetime import datetime
logging.basicConfig(level=logging.INFO)


class Database:
    def __init__(self, path_to_db="main.db"):
        self.path_to_db = path_to_db
        self.create_table_bot_info()

    @property
    def connection(self):
        return sqlite3.connect(self.path_to_db)

    def execute(self, sql: str, parameters: tuple = None, fetchone=False, fetchall=False, commit=False):
        if not parameters:
            parameters = ()
        connection = self.connection
        cursor = connection.cursor()
        data = None
        cursor.execute(sql, parameters)

        if commit:
            connection.commit()
        if fetchall:
            data = cursor.fetchall()
        if fetchone:
            data = cursor.fetchone()
        connection.close()
        return data

    def create_table_bot_info(self):
        sql = """
        CREATE TABLE IF NOT EXISTS BotInfo(
        start_time TEXT
        );
        """
        self.execute(sql, commit=True)
        # Agar `BotInfo` jadvali bo'sh bo'lsa, botning ishga tushgan vaqtini qo'shing
        if not self.execute("SELECT * FROM BotInfo;", fetchone=True):
            self.execute("INSERT INTO BotInfo (start_time) VALUES (?);", parameters=(datetime.now().isoformat(),), commit=True)

    def get_bot_start_time(self):
        return self.execute("SELECT start_time FROM BotInfo;", fetchone=True)[0]

    def count_users(self):
        return self.execute("SELECT COUNT(*) FROM Users;", fetchone=True)

db = Database()

async def get_bot_statistics():
    total_users = db.count_users()[0]
    bot_start_time = db.get_bot_start_time()
    start_time = datetime.fromisoformat(bot_start_time)
    uptime = datetime.now() - start_time
    days_uptime = uptime.days
    
    # Uptime formatlash
    hours, remainder = divmod(uptime.seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    formatted_uptime = f"{days_uptime} kun, {hours} soat, {minutes} daqiqa, {seconds} soniya"
    
    error_count = 0  # Bu qiymatni haqiqiy xatoliklar bilan almashtiring

    return {
        "total_users": total_users,
        "error_count": error_count,
        "uptime": formatted_uptime,
        "days_uptime": days_uptime
    }

@dp.message(Command("stats"))
async def show_bot_statistics(message:Message):
    stats = await get_bot_statistics()
    
    response = (
        f"👥 *Jami foydalanuvchilar:* {stats['total_users']}\n\n"
        f"⚠️ *Bot xatoliklari:* {stats['error_count']}\n\n"
        f"⏳ *Bot ishga tushgan vaqt:* {stats['uptime']}\n\n"
        f"📅 *Kunlar soni:* {stats['days_uptime']}"
    )
    
    # Rasmning URL manzili
    photo_url = "https://static3.tgstat.ru/channels/_0/7a/7a13404ed6199848a0dd561a94567e60.jpg"
    
    # Rasmni yuborish
    await message.answer_photo(photo=photo_url, caption=response, parse_mode='Markdown')