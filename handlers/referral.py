"""
Referral handler
"""
import logging
from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import Command
from database import db
from config import CURRENCY_SYMBOL, REFERRAL_BONUS

logger = logging.getLogger(__name__)
router = Router()


@router.message(Command("referral"))
@router.message(F.text == "👥 Referrals")
async def referral_command(message: Message):
    """Handle referral command"""
    user_id = message.from_user.id
    
    if not db.user_exists(user_id):
        user = db.create_user(user_id, message.from_user.username, message.from_user.first_name)
    else:
        user = db.get_user(user_id)
    
    referrals = db.get_referrals(user_id)
    earnings = len(referrals) * REFERRAL_BONUS
    
    text = f"👥 Referral Program\n\nCode: {user.referral_code}\nFriends: {len(referrals)}\nEarnings: {earnings} {CURRENCY_SYMBOL}\n\nShare to earn more!"
    await message.answer(text)
