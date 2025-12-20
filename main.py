import asyncio
import logging
from aiogram import Dispatcher, Bot
from config import API_TOKEN
from database import create_table
from handlers import register_handlers

logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN)
dp = Dispatcher()

register_handlers(dp)

async def main():
    await create_table()
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())