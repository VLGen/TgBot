import asyncio
import logging
from aiogram import Dispatcher, Bot
from config import config
from database import create_table
from handlers import register_handlers

logging.basicConfig(level=logging.INFO)

print("BOT_TOKEN RAW:", config.bot_token)
print("BOT_TOKEN VALUE:", None if config.bot_token is None else config.bot_token.get_secret_value())
print("DB:", config.db)

bot = Bot(token=config.bot_token.get_secret_value()) # type: ignore
dp = Dispatcher()

register_handlers(dp)

async def main():
    await create_table()
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())