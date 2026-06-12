"""
Tasks handler
"""
import logging
from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
from database import db
from config import TASK_REWARDS, CURRENCY_SYMBOL
from utils.keyboards import get_tasks_keyboard, get_back_button

logger = logging.getLogger(__name__)
router = Router()


@router.message(Command("tasks"))
@router.message(F.text == "✅ Tasks")
async def tasks_command(message: Message):
    """Handle tasks command"""
    user_id = message.from_user.id
    
    if not db.user_exists(user_id):
        db.create_user(user_id, message.from_user.username, message.from_user.first_name)
    
    tasks_text = "✅ Available Tasks\n\n"
    for task_type, reward in TASK_REWARDS.items():
        tasks_text += f"• {task_type}: +{reward} {CURRENCY_SYMBOL}\n"
    
    await message.answer(tasks_text, reply_markup=get_tasks_keyboard())


@router.callback_query(F.data == "task_daily")
async def task_daily_callback(callback: CallbackQuery):
    """Handle daily task"""
    user_id = callback.from_user.id
    reward = TASK_REWARDS.get("daily_checkin", 50)
    
    task = db.create_task(user_id, "daily_checkin", reward)
    user = db.update_balance(user_id, reward)
    db.complete_task(task.id)
    
    text = f"✅ Daily Check-in Complete!\n+{reward} {CURRENCY_SYMBOL}\nBalance: {user.balance} {CURRENCY_SYMBOL}"
    await callback.answer(f"+{reward} {CURRENCY_SYMBOL}", show_alert=True)
    await callback.message.edit_text(text, reply_markup=get_back_button())


@router.callback_query(F.data == "task_invite")
async def task_invite_callback(callback: CallbackQuery):
    """Handle invite task"""
    user_id = callback.from_user.id
    user = db.get_user(user_id)
    referrals = db.get_referrals(user_id)
    
    text = f"👥 Invite Friends\n\nCode: {user.referral_code}\nFriends: {len(referrals)}"
    await callback.answer()
    await callback.message.edit_text(text, reply_markup=get_back_button())
