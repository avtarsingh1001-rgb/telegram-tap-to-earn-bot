"""
Helper functions for the Telegram Tap-to-Earn Bot
"""
import time
from typing import Dict
from config import TAP_COOLDOWN, CURRENCY_SYMBOL, CURRENCY_NAME

user_cooldowns: Dict[int, float] = {}


def check_tap_cooldown(user_id: int) -> tuple:
    """Check if user can tap"""
    current_time = time.time()
    last_tap = user_cooldowns.get(user_id, 0)
    remaining = TAP_COOLDOWN - (current_time - last_tap)
    
    if remaining <= 0:
        user_cooldowns[user_id] = current_time
        return True, 0
    
    return False, remaining


def format_balance(balance: int) -> str:
    """Format balance with currency symbol"""
    return f"{balance} {CURRENCY_SYMBOL} {CURRENCY_NAME}"
