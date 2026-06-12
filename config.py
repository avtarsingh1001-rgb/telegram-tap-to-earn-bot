"""
Configuration and constants for the Telegram Tap-to-Earn Bot
"""
import os
from dotenv import load_dotenv

load_dotenv()

# Bot Configuration
BOT_TOKEN = os.getenv("BOT_TOKEN", "YOUR_BOT_TOKEN_HERE")
DATABASE_FILE = "database.db"

# Game Configuration
STARTING_BALANCE = 1000
TAP_REWARD = 1
DAILY_BONUS = 100
REFERRAL_BONUS = 500
REFERRED_BONUS = 100

# Rate Limiting
TAP_COOLDOWN = 1
TASK_DAILY_LIMIT = 5
REQUEST_TIMEOUT = 30

# Leaderboard
TOP_USERS_COUNT = 10

# Logging
LOG_LEVEL = "INFO"
LOG_FILE = "bot.log"

# Currency Settings
CURRENCY_NAME = "COINS"
CURRENCY_SYMBOL = "💰"

# Task Rewards (in coins)
TASK_REWARDS = {
    "daily_checkin": 50,
    "invite_friend": 200,
    "watch_video": 75,
    "survey": 100,
    "share_bot": 150,
}
