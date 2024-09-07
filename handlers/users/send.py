import asyncio
from datetime import datetime, timedelta
from aiogram import F, Bot
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from loader import dp, bot, CHANNELS, ADMINS
from states.reklama import SendState
from keyboard_buttons.admin_keyboard import confirmation
from filters.admin import IsBotAdminFilter

class ValidationError(Exception):
    pass

@dp.message(Command("send"), IsBotAdminFilter(ADMINS))
async def start_sending(message: Message, state: FSMContext):
    if message.from_user.id in ADMINS:
        await message.reply("Xabar, rasm yoki video yuboring")
        await state.set_state(SendState.ask)
    else:
        await message.reply("Sizda ushbu komanda uchun ruxsat yo'q.")

@dp.message(SendState.ask, IsBotAdminFilter(ADMINS))
async def handle_media(message: Message, state: FSMContext):
    if message.text:
        await state.update_data(type_send="text", text=message.text)
        await message.answer("Xabar qachon yuborilsin? (Masalan: 13:05)")
        await state.set_state(SendState.time)

    elif message.photo:
        photo = message.photo[-1].file_id
        photo_txt = message.caption or ""
        await state.update_data(type_send="photo", photo=photo, photo_txt=photo_txt)
        await message.answer("Rasm qachon yuborilsin? (Masalan: 13:05)")
        await state.set_state(SendState.time)

    elif message.video:
        video = message.video.file_id
        video_txt = message.caption or ""
        await state.update_data(type_send="video", video=video, video_txt=video_txt)
        await message.answer("Video qachon yuborilsin? (Masalan: 13:05)")
        await state.set_state(SendState.time)

    else:
        await message.reply("Yuborilgan format qo'llab-quvvatlanmaydi.")
        return

@dp.message(SendState.time, IsBotAdminFilter(ADMINS))
async def handle_time(message: Message, state: FSMContext):
    time = message.text.strip()

    try:
        hour, minute = map(int, time.split(":"))
        if 0 <= hour < 24 and 0 <= minute < 60:
            now = datetime.now()
            send_time = now.replace(hour=hour, minute=minute, second=0, microsecond=0)

            if send_time < now:
                send_time += timedelta(days=1)

            await state.update_data(send_time=send_time.strftime('%Y-%m-%d %H:%M:%S'))
            data = await state.get_data()
            type_send = data.get("type_send")

            if type_send == "text":
                send_text = f"Xabar Kanalga {time} da yuborilsinmi!\n\n{data.get('text')}"
                await message.answer(send_text, reply_markup=confirmation)

            elif type_send == "photo":
                photo_txt = data.get("photo_txt")
                send_text = f"Rasm Kanalga {time} da yuborilsinmi!\n\n{photo_txt}"
                await message.answer_photo(data.get("photo"), caption=send_text, reply_markup=confirmation)

            elif type_send == "video":
                video_txt = data.get("video_txt")
                send_text = f"Video Kanalga {time} da yuborilsinmi!\n\n{video_txt}"
                await message.answer_video(data.get("video"), caption=send_text, reply_markup=confirmation)

            await state.set_state(SendState.confirm)

        else:
            raise ValidationError

    except (ValueError, ValidationError):
        await message.reply("Noto'g'ri format, iltimos, vaqtni HH:MM formatida kiriting.")

@dp.callback_query(SendState.confirm, F.data == "right", IsBotAdminFilter(ADMINS))
async def confirm_send(callback: CallbackQuery, state: FSMContext):
    await callback.message.delete()
    data = await state.get_data()
    type_send = data.get("type_send")
    send_time_str = data.get("send_time")
    send_time = datetime.strptime(send_time_str, '%Y-%m-%d %H:%M:%S')
    now = datetime.now()

    wait_time = (send_time - now).total_seconds()
    if wait_time > 0:
        await asyncio.sleep(wait_time)

    if type_send == "text":
        text = data.get("text")
        await bot.send_message(CHANNELS[0], text)
        await bot.send_message(ADMINS[0], f"Yuborilgan xabar:\n{text}")

    elif type_send == "photo":
        photo = data.get("photo")
        photo_txt = data.get("photo_txt")
        await bot.send_photo(CHANNELS[0], photo, caption=photo_txt)
        await bot.send_photo(ADMINS[0], photo, caption=photo_txt)

    elif type_send == "video":
        video = data.get("video")
        video_txt = data.get("video_txt")
        await bot.send_video(CHANNELS[0], video, caption=video_txt)
        await bot.send_video(ADMINS[0], video, caption=video_txt)

    else:
        await callback.message.answer("Yuborilgan format qo'llab-quvvatlanmaydi.")
        await state.clear()
        return

    await callback.message.answer("Xabar muvaffaqiyatli kanalga yuborildi 🎉🎉🎉")
    await state.clear()

@dp.callback_query(SendState.confirm, F.data == "cancel", IsBotAdminFilter(ADMINS))
async def cancel_send(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    await callback.message.delete()
    await callback.answer("Yuborilmadi ❌", reply_markup=None)
