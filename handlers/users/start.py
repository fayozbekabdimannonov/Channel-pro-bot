from aiogram.types import Message
from loader import dp,db
from aiogram.filters import CommandStart
from keyboard_buttons.admin_keyboard import admin_button1

@dp.message(CommandStart())
async def start_command(message:Message):
    full_name = message.from_user.full_name
    telegram_id = message.from_user.id
    try:
        db.add_user(full_name=full_name,telegram_id=telegram_id) #foydalanuvchi bazaga qo'shildi
        await message.answer(text="startga nimadir yoziladi",reply_markup=admin_button1)
    except:
        await message.answer(text="startga nimadir yoziladi",reply_markup=admin_button1)
