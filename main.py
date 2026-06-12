"""
Main entry point for the Telegram Tap-to-Earn Bot
"""
import asyncio
import logging
from aiogram import Dispatcher, Bot
from aiogram.types import BotCommand, BotCommandScopeDefault
from config import BOT_TOKEN, LOG_LEVEL, LOG_FILE
from handlers import start, tap, stats, leaderboard, tasks, referral

# Configure logging
logging.basicConfig(
    level=getattr(logging, LOG_LEVEL),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(LOG_FILE),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


async def set_commands(bot: Bot):
    """Set bot commands"""
    commands = [
        BotCommand(command="start", description="Start the bot"),
        BotCommand(command="tap", description="Tap to earn coins"),
        BotCommand(command="stats", description="View statistics"),
        BotCommand(command="leaderboard", description="View leaderboard"),
        BotCommand(command="tasks", description="View tasks"),
        BotCommand(command="referral", description="View referral info"),
    ]
    await bot.set_my_commands(commands, BotCommandScopeDefault())
    logger.info("Bot commands set successfully")


async def main():
    """Main bot function"""
    bot = Bot(token=BOT_TOKEN)
    dp = Dispatcher()
    
    # Register handlers
    dp.include_router(start.router)
    dp.include_router(tap.router)
    dp.include_router(stats.router)
    dp.include_router(leaderboard.router)
    dp.include_router(tasks.router)
    dp.include_router(referral.router)
    
    # Set bot commands
    await set_commands(bot)
    
    logger.info("Bot started successfully!")
    
    try:
        await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())
    finally:
        await bot.session.close()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Bot stopped by user")
