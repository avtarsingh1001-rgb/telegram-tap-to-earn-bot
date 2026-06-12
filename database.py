"""
Database operations for the Telegram Tap-to-Earn Bot
"""
import sqlite3
from datetime import datetime
from typing import Optional, List
from models import User, Task, Referral, Leaderboard
from config import DATABASE_FILE, STARTING_BALANCE
import uuid
import logging

logger = logging.getLogger(__name__)


class Database:
    """Database manager for the bot"""
    
    def __init__(self, db_file: str = DATABASE_FILE):
        self.db_file = db_file
        self.init_db()
    
    def get_connection(self):
        """Get database connection"""
        return sqlite3.connect(self.db_file)
    
    def init_db(self):
        """Initialize database tables"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # Users table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER UNIQUE NOT NULL,
                username TEXT,
                first_name TEXT,
                balance INTEGER DEFAULT 0,
                total_earned INTEGER DEFAULT 0,
                taps INTEGER DEFAULT 0,
                referral_code TEXT UNIQUE,
                referred_by INTEGER,
                last_tap TIMESTAMP,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Tasks table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                task_type TEXT NOT NULL,
                completed BOOLEAN DEFAULT 0,
                reward INTEGER DEFAULT 0,
                completed_at TIMESTAMP,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(user_id)
            )
        ''')
        
        # Referrals table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS referrals (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                referrer_id INTEGER NOT NULL,
                referred_id INTEGER NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (referrer_id) REFERENCES users(user_id),
                FOREIGN KEY (referred_id) REFERENCES users(user_id)
            )
        ''')
        
        conn.commit()
        conn.close()
        logger.info("Database initialized successfully")
    
    def user_exists(self, user_id: int) -> bool:
        """Check if user exists"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT 1 FROM users WHERE user_id = ?', (user_id,))
        result = cursor.fetchone() is not None
        conn.close()
        return result
    
    def create_user(self, user_id: int, username: Optional[str] = None, 
                   first_name: Optional[str] = None, referred_by: Optional[int] = None) -> User:
        """Create a new user"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        referral_code = str(uuid.uuid4())[:8].upper()
        
        cursor.execute('''
            INSERT INTO users 
            (user_id, username, first_name, balance, referral_code, referred_by)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (user_id, username, first_name, STARTING_BALANCE, referral_code, referred_by))
        
        conn.commit()
        conn.close()
        logger.info(f"User {user_id} created with starting balance {STARTING_BALANCE}")
        
        return self.get_user(user_id)
    
    def get_user(self, user_id: int) -> Optional[User]:
        """Get user by ID"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM users WHERE user_id = ?', (user_id,))
        row = cursor.fetchone()
        conn.close()
        
        if not row:
            return None
        
        return User(
            user_id=row[1],
            username=row[2],
            first_name=row[3],
            balance=row[4],
            total_earned=row[5],
            taps=row[6],
            referral_code=row[7],
            referred_by=row[8],
            last_tap=row[9],
            created_at=row[10]
        )
    
    def update_balance(self, user_id: int, amount: int) -> User:
        """Update user balance"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            UPDATE users 
            SET balance = balance + ?, total_earned = total_earned + ?
            WHERE user_id = ?
        ''', (amount, amount if amount > 0 else 0, user_id))
        
        conn.commit()
        conn.close()
        
        return self.get_user(user_id)
    
    def update_taps(self, user_id: int, taps: int = 1) -> User:
        """Update user taps count"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            UPDATE users 
            SET taps = taps + ?, last_tap = CURRENT_TIMESTAMP
            WHERE user_id = ?
        ''', (taps, user_id))
        
        conn.commit()
        conn.close()
        
        return self.get_user(user_id)
    
    def get_leaderboard(self, limit: int = 10) -> List[Leaderboard]:
        """Get top users leaderboard"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT user_id, username, balance, total_earned, taps
            FROM users
            ORDER BY balance DESC
            LIMIT ?
        ''', (limit,))
        
        rows = cursor.fetchall()
        conn.close()
        
        leaderboard = []
        for rank, row in enumerate(rows, 1):
            leaderboard.append(Leaderboard(
                rank=rank,
                user_id=row[0],
                username=row[1] or f"User{row[0]}",
                balance=row[2],
                total_earned=row[3],
                taps=row[4]
            ))
        
        return leaderboard
    
    def create_task(self, user_id: int, task_type: str, reward: int) -> Task:
        """Create a new task"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO tasks (user_id, task_type, reward)
            VALUES (?, ?, ?)
        ''', (user_id, task_type, reward))
        
        conn.commit()
        task_id = cursor.lastrowid
        conn.close()
        
        return self.get_task(task_id)
    
    def get_task(self, task_id: int) -> Optional[Task]:
        """Get task by ID"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM tasks WHERE id = ?', (task_id,))
        row = cursor.fetchone()
        conn.close()
        
        if not row:
            return None
        
        return Task(
            id=row[0],
            user_id=row[1],
            task_type=row[2],
            completed=bool(row[3]),
            reward=row[4],
            completed_at=row[5],
            created_at=row[6]
        )
    
    def complete_task(self, task_id: int) -> Task:
        """Mark task as completed"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            UPDATE tasks 
            SET completed = 1, completed_at = CURRENT_TIMESTAMP
            WHERE id = ?
        ''', (task_id,))
        
        conn.commit()
        conn.close()
        
        return self.get_task(task_id)
    
    def get_referrals(self, user_id: int) -> List[int]:
        """Get list of users referred by this user"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT referred_id FROM referrals WHERE referrer_id = ?', (user_id,))
        rows = cursor.fetchall()
        conn.close()
        
        return [row[0] for row in rows]


db = Database()
