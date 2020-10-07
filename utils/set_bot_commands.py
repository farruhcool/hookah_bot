from aiogram import types


async def set_default_commands(dp):
    await dp.bot.set_my_commands([
        types.BotCommand("start", "Запустить бота"),
        types.BotCommand("help", "Помощь"),
        types.BotCommand("tel", "Ввести телефонный номер"),
        types.BotCommand("send_location", "Ввести телефонный номер"),
    ])
