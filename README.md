# Telegram Tap-to-Earn Bot Clone

A feature-rich Telegram bot that rewards users for tapping/clicking with in-game currency. Users can earn coins, complete tasks, refer friends, and participate in leaderboards.

## Features

- **Tap-to-Earn Mechanics**: Users earn coins by tapping a button
- **User Balance System**: Track user balances and statistics
- **Daily Rewards**: Bonus coins for daily check-ins
- **Referral System**: Earn coins by inviting friends
- **Leaderboard**: Compete with other users
- **Task System**: Complete tasks for extra rewards
- **Passive Income**: Mining system for continuous earning
- **User Persistence**: SQLite database to store user data
- **Statistics**: Track user stats and progress

## Tech Stack

- **Language**: Python 3.9+
- **Bot Framework**: aiogram 3.x (async Telegram Bot API)
- **Database**: SQLite3
- **Async Support**: asyncio

## Installation

### Prerequisites
- Python 3.9 or higher
- pip (Python package manager)
- Telegram Bot API token (create via @BotFather)

### Setup Steps

1. **Clone the repository**
```bash
git clone https://github.com/avtarsingh1001-rgb/telegram-tap-to-earn-bot.git
cd telegram-tap-to-earn-bot
```

2. **Create a virtual environment**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Configure the bot**
```bash
cp .env.example .env
# Edit .env and add your BOT_TOKEN
```

5. **Run the bot**
```bash
python main.py
```

## Configuration

Edit `config.py` to customize:
- Bot token
- Starting balance
- Tap reward amount
- Daily bonus
- Referral bonus

## Usage

### Commands
- `/start` - Start the bot
- `/tap` - Tap to earn coins
- `/stats` - View statistics
- `/leaderboard` - View top earners
- `/tasks` - View tasks
- `/referral` - View referral info
- `/help` - Get help

## Project Structure

```
telegram-tap-to-earn-bot/
├── config.py
├── database.py
├── models.py
├── handlers/
│   ├── start.py
│   ├── tap.py
│   ├── stats.py
│   ├── leaderboard.py
│   ├── tasks.py
│   └── referral.py
├── utils/
│   ├── keyboards.py
│   └── helpers.py
├── main.py
├── requirements.txt
└── .env.example
```

## Deployment

### Docker
```bash
docker build -t tap-to-earn-bot .
docker run -e BOT_TOKEN=your_token tap-to-earn-bot
```

### Cloud Platforms
- Heroku, Railway, AWS Lambda, Google Cloud Run, DigitalOcean

## Security

- Never commit BOT_TOKEN to repository
- Use environment variables for sensitive data
- Implement rate limiting to prevent abuse

## License

MIT License
