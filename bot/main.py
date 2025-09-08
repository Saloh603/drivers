import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram.types import BotCommand
from aiogram.client.default import DefaultBotProperties
from bot.db import init_db

# Import handlers
from bot.handlers import start, driver, passenger

logging.basicConfig(level=logging.INFO)

TOKEN = "7822007401:AAFMX-Mj8lcNP8NcUHbo_4Z9E199mSMmN0g"

async def main():
    # Init DB
    await init_db()

    # Setup bot
    bot = Bot(
        token=TOKEN,
        default=DefaultBotProperties(parse_mode="HTML")
    )
    dp = Dispatcher()

    # Register handlers
    dp.include_router(start.router)
    dp.include_router(driver.router)
    dp.include_router(passenger.router)

    # Set bot commands
    await bot.set_my_commands([
        BotCommand(command="start", description="Start the bot")
    ])

    # Start polling
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
