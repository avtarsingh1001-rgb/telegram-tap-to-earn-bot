"""
Start command handler
"""
import logging
from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart, Command
from database import db
from config import STARTING_BALANCE, CURRENCY_SYMBOL
from utils.keyboards import get_main_menu_keyboard, get_tap_keyboard

logger = logging.getLogger(__name__)
router = Router()


@router.message(CommandStart())
async def start_command(message: Message):
    """Handle /start command"""
    user_id = message.from_user.id
    username = message.from_user.username
    first_name = message.from_user.first_name
    
    if not db.user_exists(user_id):
        user = db.create_user(user_id, username, first_name)
        welcome_text = f"🎉 Welcome to Tap-to-Earn Bot!\n\nYou received: 💰 {STARTING_BALANCE} {CURRENCY_SYMBOL}\n\nStart tapping to earn more!"
        await message.answer(welcome_text, reply_markup=get_main_menu_keyboard())
    else:
        user = db.get_user(user_id)
        welcome_back_text = f"👋 Welcome back!\n\nBalance: {user.balance} {CURRENCY_SYMBOL}"
        await message.answer(welcome_back_text, reply_markup=get_main_menu_keyboard())
