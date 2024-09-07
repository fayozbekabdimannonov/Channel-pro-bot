from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton,ReplyKeyboardMarkup, KeyboardButton
admin_button = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Foydalanuvchilar soni"),
            KeyboardButton(text="Reklama yuborish"),
        ]
        
    ],
   resize_keyboard=True,
   input_field_placeholder="Menudan birini tanlang"
)
confirmation = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text= "Bekor qilish ❌", callback_data="cancel"), InlineKeyboardButton(text= "Tasdiqlash ✅", callback_data="right")],

    ]
)

orqaga_button = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="♻️ Orqaga"),        
        ]      
    ],
  resize_keyboard=True
)
admin_button1 = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="👨‍💼Admin"),        
        ]      
    ],
  resize_keyboard=True
)
