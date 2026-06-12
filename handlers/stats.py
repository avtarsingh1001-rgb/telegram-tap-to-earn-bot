"""
Stats handler
"""
import logging
from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
from database import db
from config import CURRENCY_SYMBOL
from utils.keyboards import get_stats_keyboard, get_main_menu_keyboard

logger = logging.getLogger(__name__)
router = Router()


@router.message(Command("stats"))
@router.message(F.text == "📊 Stats")
async def stats_command(message: Message):
    """Handle stats command"""
    user_id = message.from_user.id
    
    if not db.user_exists(user_id):
        db.create_user(user_id, message.from_user.username, message.from_user.first_name)
    
    user = db.get_user(user_id)
    stats_text = f"📊 Your Statistics\n\nBalance: {user.balance} {CURRENCY_SYMBOL}\nTotal Earned: {user.total_earned} {CURRENCY_SYMBOL}\nTaps: {user.taps}"
    await message.answer(stats_text, reply_markup=get_stats_keyboard())


@router.callback_query(F.data == "balance")
async def balance_callback(callback: CallbackQuery):
    """Handle balance button"""
    user_id = callback.from_user.id
    user = db.get_user(user_id)
    await callback.answer(f"Balance: {user.balance} {CURRENCY_SYMBOL}", show_alert=False)


@router.callback_query(F.data == "stats_details")
async def stats_details_callback(callback: CallbackQuery):
    """Handle stats details button"""
    user_id = callback.from_user.id
    user = db.get_user(user_id)
    text = f"📊 Statistics\nBalance: {user.balance}\nEarned: {user.total_earned}\nTaps: {user.taps}"
    await callback.answer()
    await callback.message.edit_text(text)
