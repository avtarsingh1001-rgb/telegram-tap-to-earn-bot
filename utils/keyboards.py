"""
Keyboard layouts for the Telegram Tap-to-Earn Bot
"""
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton
from config import CURRENCY_SYMBOL


def get_main_menu_keyboard() -> ReplyKeyboardMarkup:
    """Get main menu keyboard"""
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="👆 TAP")],
            [KeyboardButton(text="📊 Stats"), KeyboardButton(text="🏆 Leaderboard")],
            [KeyboardButton(text="✅ Tasks"), KeyboardButton(text="👥 Referrals")],
            [KeyboardButton(text="❓ Help")]
        ],
        resize_keyboard=True
    )
    return keyboard


def get_tap_keyboard() -> InlineKeyboardMarkup:
    """Get tap button keyboard"""
    return InlineKeyboardMarkup(
        inline_keyboard=[[InlineKeyboardButton(text="👆 TAP!", callback_data="tap")]]
    )


def get_stats_keyboard() -> InlineKeyboardMarkup:
    """Get stats keyboard"""
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="💰 Balance", callback_data="balance")],
            [InlineKeyboardButton(text="📈 Details", callback_data="stats_details")],
        ]
    )


def get_tasks_keyboard() -> InlineKeyboardMarkup:
    """Get tasks keyboard"""
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Daily Check-in", callback_data="task_daily")],
            [InlineKeyboardButton(text="Invite Friends", callback_data="task_invite")],
        ]
    )


def get_back_button() -> InlineKeyboardMarkup:
    """Get back button"""
    return InlineKeyboardMarkup(
        inline_keyboard=[[InlineKeyboardButton(text="🔙 Back", callback_data="back")]]
    )
