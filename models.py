"""
Data models for the Telegram Tap-to-Earn Bot
"""
from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class User:
    """User model"""
    user_id: int
    username: Optional[str] = None
    first_name: Optional[str] = None
    balance: int = 0
    total_earned: int = 0
    taps: int = 0
    referral_code: Optional[str] = None
    referred_by: Optional[int] = None
    last_tap: Optional[datetime] = None
    created_at: Optional[datetime] = None


@dataclass
class Task:
    """Task model"""
    id: int
    user_id: int
    task_type: str
    completed: bool = False
    reward: int = 0
    completed_at: Optional[datetime] = None
    created_at: Optional[datetime] = None


@dataclass
class Referral:
    """Referral model"""
    id: int
    referrer_id: int
    referred_id: int
    created_at: Optional[datetime] = None


@dataclass
class Leaderboard:
    """Leaderboard entry"""
    rank: int
    user_id: int
    username: str
    balance: int
    total_earned: int
    taps: int
