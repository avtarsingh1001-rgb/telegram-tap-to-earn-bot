"""
Leaderboard handler
"""
import logging
from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import Command
from database import db
from config import TOP_USERS_COUNT, CURRENCY_SYMBOL

logger = logging.getLogger(__name__)
router = Router()


@router.message(Command("leaderboard"))
@router.message(F.text == "🏆 Leaderboard")
async def leaderboard_command(message: Message):
    """Handle leaderboard command"""
    user_id = message.from_user.id
    
    if not db.user_exists(user_id):
        db.create_user(user_id, message.from_user.username, message.from_user.first_name)
    
    leaderboard = db.get_leaderboard(TOP_USERS_COUNT)
    
    if not leaderboard:
        text = "📊 Leaderboard\n\nNo entries yet!"
    else:
        text = "🏆 Top Earners\n\n"
        medals = ["🥇", "🥈", "🥉"]
        for entry in leaderboard:
            medal = medals[entry.rank - 1] if entry.rank <= 3 else f"{entry.rank}."
            text += f"{medal} {entry.username}: {entry.balance} {CURRENCY_SYMBOL}\n"
    
    await message.answer(text)
