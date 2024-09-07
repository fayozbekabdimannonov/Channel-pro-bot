from aiogram import Bot
from aiogram.methods.set_my_commands import BotCommand
from aiogram.types import BotCommandScopeAllPrivateChats


async def set_default_commands(bot: Bot):
    commands = [
        BotCommand(command="/start", description="Botni ishga tushirish"),
        BotCommand(command="/help", description="Yordam"),
        BotCommand(command="/send", description="Kanalga xabar yuborish"),
        BotCommand(command="/about", description="Biz haqimizda"),
        BotCommand(command="/last_send_message", description="Kanaldagi ohirgi yuborilgan habar"),
        BotCommand(command="/changephoto", description="rasm o'zgartirish"),
        BotCommand(command="/changename", description="title o'zgartirish"),
    ]
    await bot.set_my_commands(commands=commands, scope=BotCommandScopeAllPrivateChats())