"""
Tap handler
"""
import logging
from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
from database import db
from config import TAP_REWARD, CURRENCY_SYMBOL
from utils.keyboards import get_tap_keyboard
from utils.helpers import check_tap_cooldown

logger = logging.getLogger(__name__)
router = Router()


@router.message(Command("tap"))
@router.message(F.text == "👆 TAP")
async def tap_command(message: Message):
    """Handle tap command"""
    user_id = message.from_user.id
    
    if not db.user_exists(user_id):
        db.create_user(user_id, message.from_user.username, message.from_user.first_name)
    
    can_tap, remaining = check_tap_cooldown(user_id)
    
    if not can_tap:
        await message.answer(f"⏳ Wait {remaining:.1f}s", reply_markup=get_tap_keyboard())
        return
    
    user = db.update_balance(user_id, TAP_REWARD)
    user = db.update_taps(user_id, 1)
    
    tap_text = f"👆 TAP!\n+{TAP_REWARD} {CURRENCY_SYMBOL}\nBalance: {user.balance} {CURRENCY_SYMBOL}"
    await message.answer(tap_text, reply_markup=get_tap_keyboard())
    logger.info(f"User {user_id} tapped! Balance: {user.balance}")


@router.callback_query(F.data == "tap")
async def tap_callback(callback: CallbackQuery):
    """Handle tap button"""
    user_id = callback.from_user.id
    
    if not db.user_exists(user_id):
        db.create_user(user_id, callback.from_user.username, callback.from_user.first_name)
    
    can_tap, remaining = check_tap_cooldown(user_id)
    
    if not can_tap:
        await callback.answer(f"⏳ Wait {remaining:.1f}s", show_alert=False)
        return
    
    user = db.update_balance(user_id, TAP_REWARD)
    user = db.update_taps(user_id, 1)
    
    tap_text = f"👆 TAP!\n+{TAP_REWARD} {CURRENCY_SYMBOL}\nBalance: {user.balance} {CURRENCY_SYMBOL}"
    await callback.answer(f"+{TAP_REWARD} {CURRENCY_SYMBOL}", show_alert=False)
    await callback.message.edit_text(tap_text, reply_markup=get_tap_keyboard())
