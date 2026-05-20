#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
╔══════════════════════════════════════════════════════════════════╗
║           SIMURAZX PTERODACTYL BOTz v1.0                         ║
║         Optimized for Pterodactyl Panel                          ║
║                      Mode: UNRESTRICTED                          ║
╚══════════════════════════════════════════════════════════════════╝
"""

import asyncio
import aiohttp
import random
import json
import os
import time
import sys
from datetime import datetime, timedelta
from typing import Dict, List, Tuple, Optional
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, BotCommand
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters, ContextTypes
import logging

# ==================== KONFIGURASI PTERODACTYL ====================
# Gunakan environment variable untuk keamanan
BOT_TOKEN = os.environ.get("BOT_TOKEN", "8322931459:AAGh8F95PpBo8xDCHSyXrtAH8_OG1LSmSu4")
ADMIN_IDS = [int(x) for x in os.environ.get("ADMIN_IDS", "7001994316").split(",")]
VERSION = "SIMURAZX PTERODACTYL v1.0"
BOT_NAME = "SimurazxBotz"

# Konfigurasi Pterodactyl
DATA_DIR = os.path.join(os.path.dirname(__file__), "data")
USERS_FILE = os.path.join(DATA_DIR, "users.json")
STATS_FILE = os.path.join(DATA_DIR, "stats.json")

# Buat direktori data jika belum ada
os.makedirs(DATA_DIR, exist_ok=True)

# Logging untuk Pterodactyl (output ke console)
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler(sys.stdout)]
)
logger = logging.getLogger(__name__)

# ==================== ICON & EMOJI ====================
ICON = {
    "main": "👑", "bot": "🤖", "fire": "🔥", "crown": "🏆",
    "star": "⭐", "heart": "💖", "rocket": "🚀", "target": "🎯",
    "clock": "⏱️", "cpu": "💻", "network": "🌐", "success": "✅",
    "error": "❌", "warn": "⚠️", "info": "ℹ️", "menu": "📋",
    "settings": "⚙️", "user": "👤", "game": "🎮", "tools": "🛠️",
    "back": "🔙", "home": "🏠", "dice": "🎲", "sword": "⚔️",
    "magic": "🔮", "trophy": "🏆", "link": "🔗", "search": "🔍"
}

# ==================== DATA STORAGE ====================

def load_users():
    """Load user data from JSON file"""
    if os.path.exists(USERS_FILE):
        with open(USERS_FILE, 'r') as f:
            return json.load(f)
    return {}

def save_users(users):
    """Save user data to JSON file"""
    with open(USERS_FILE, 'w') as f:
        json.dump(users, f, indent=2)

def load_stats():
    """Load statistics from JSON file"""
    if os.path.exists(STATS_FILE):
        with open(STATS_FILE, 'r') as f:
            return json.load(f)
    return {"start_time": time.time(), "total_commands": 0, "total_users": 0}

def save_stats(stats):
    """Save statistics to JSON file"""
    with open(STATS_FILE, 'w') as f:
        json.dump(stats, f, indent=2)

# Load data
user_data = load_users()
bot_stats = load_stats()

# ==================== KELAS BOT ====================

class SimurazxBot:
    def __init__(self, token: str):
        self.token = token
        self.app = None
        self.start_time = time.time()
    
    def _create_keyboard(self, buttons: List[Tuple[str, str]], row_width: int = 2) -> InlineKeyboardMarkup:
        """Create inline keyboard"""
        keyboard = []
        row = []
        for i, (text, callback) in enumerate(buttons):
            row.append(InlineKeyboardButton(text, callback_data=callback))
            if (i + 1) % row_width == 0 or i == len(buttons) - 1:
                keyboard.append(row)
                row = []
        return InlineKeyboardMarkup(keyboard)
    
    async def send_main_menu(self, update: Update, context: ContextTypes.DEFAULT_TYPE, message_id: int = None):
        """Send main menu with premium design"""
        user = update.effective_user
        user_id = str(user.id)
        
        # Update user data
        if user_id not in user_data:
            user_data[user_id] = {"name": user.first_name, "first_seen": time.time(), "commands": 0}
            bot_stats["total_users"] = len(user_data)
            save_users(user_data)
            save_stats(bot_stats)
        
        uptime = str(timedelta(seconds=int(time.time() - self.start_time)))
        
        menu_text = f"""
{ICON['crown']}{ICON['crown']}{ICON['crown']} *{BOT_NAME}* {ICON['crown']}{ICON['crown']}{ICON['crown']}
┌─────────────────────────────────────────────┐
│  {ICON['bot']} *Status:* 🟢 *ACTIVE*                    │
│  {ICON['user']} *User:* `{user.first_name}`                  │
│  {ICON['clock']} *Uptime:* `{uptime}`                      │
│  {ICON['star']} *Version:* `{VERSION}`                     │
└─────────────────────────────────────────────┘

{ICON['fire']} *WELCOME TO THE BOT* {ICON['fire']}

{ICON['menu']} *MAIN MENU*
────────────────────
{ICON['game']} 🎮 *GAMES*
{ICON['tools']} 🛠️ *UTILITIES*  
{ICON['info']} ℹ️ *INFORMATION*
{ICON['heart']} ❤️ *ABOUT*
────────────────────

💡 *Tap buttons below to explore!*
"""
        
        buttons = [
            (f"{ICON['game']} GAMES", "game_menu"),
            (f"{ICON['tools']} UTILITIES", "util_menu"),
            (f"{ICON['info']} INFO", "info_menu"),
            (f"{ICON['heart']} ABOUT", "about_menu")
        ]
        
        keyboard = self._create_keyboard(buttons, row_width=2)
        
        if message_id:
            await context.bot.edit_message_text(
                text=menu_text,
                chat_id=update.effective_chat.id,
                message_id=message_id,
                reply_markup=keyboard,
                parse_mode='Markdown'
            )
        else:
            await update.message.reply_text(
                text=menu_text,
                reply_markup=keyboard,
                parse_mode='Markdown'
            )
    
    # ==================== GAME MENU ====================
    
    async def game_menu(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Game menu"""
        query = update.callback_query
        await query.answer()
        
        game_text = f"""
{ICON['game']} *┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓*
{ICON['game']} *┃*  {ICON['star']} *GAME MENU*                     {ICON['game']} *┃*
{ICON['game']} *┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛*

Select your game:

{ICON['target']} *GUESS NUMBER* - Guess 1-100
{ICON['sword']} *ROCK PAPER SCISSORS* - Classic duel
{ICON['magic']} *RANDOM QUIZ* - Test your knowledge
{ICON['dice']} *ROLL DICE* - Test your luck
"""
        
        buttons = [
            (f"{ICON['target']} Guess Number", "game_guess"),
            (f"{ICON['sword']} RPS", "game_rps"),
            (f"{ICON['magic']} Quiz", "game_quiz"),
            (f"{ICON['dice']} Roll Dice", "game_dice"),
            (f"{ICON['home']} Main Menu", "main_menu")
        ]
        
        keyboard = self._create_keyboard(buttons, row_width=2)
        await query.edit_message_text(game_text, reply_markup=keyboard, parse_mode='Markdown')
    
    async def game_guess(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Guess number game"""
        query = update.callback_query
        await query.answer()
        
        secret = random.randint(1, 100)
        context.user_data['secret'] = secret
        context.user_data['game_active'] = 'guess'
        context.user_data['attempts'] = 0
        
        game_text = f"""
{ICON['target']} *🎮 GUESS NUMBER* {ICON['target']}

┌─────────────────────────────────────────────┐
│  I'm thinking of a number between *1-100*   │
│  Can you guess it?                          │
└─────────────────────────────────────────────┘

💡 *Type your guess as a number*
❌ *Type /cancel to quit*
"""
        
        buttons = [(f"{ICON['back']} Back", "game_menu")]
        keyboard = self._create_keyboard(buttons)
        
        await query.edit_message_text(game_text, reply_markup=keyboard, parse_mode='Markdown')
    
    async def game_rps(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Rock Paper Scissors game"""
        query = update.callback_query
        await query.answer()
        
        game_text = f"""
{ICON['sword']} *⚔️ ROCK PAPER SCISSORS* {ICON['sword']}

Choose your move:
"""
        
        buttons = [
            ("🪨 ROCK", "rps_rock"),
            ("✂️ SCISSORS", "rps_scissors"),
            ("📄 PAPER", "rps_paper"),
            (f"{ICON['back']} Back", "game_menu")
        ]
        
        keyboard = self._create_keyboard(buttons, row_width=3)
        await query.edit_message_text(game_text, reply_markup=keyboard, parse_mode='Markdown')
    
    async def process_rps(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Process RPS result"""
        query = update.callback_query
        await query.answer()
        
        player = query.data.replace("rps_", "")
        bot = random.choice(["rock", "scissors", "paper"])
        
        emoji = {"rock": "🪨", "scissors": "✂️", "paper": "📄"}
        
        if player == bot:
            result = "DRAW! 🤝"
        elif (player == "rock" and bot == "scissors") or \
             (player == "scissors" and bot == "paper") or \
             (player == "paper" and bot == "rock"):
            result = "YOU WIN! 🎉"
        else:
            result = "BOT WINS! 💀"
        
        result_text = f"""
{ICON['sword']} *⚔️ RESULT* {ICON['sword']}

┌─────────────────────────────────────────────┐
│  You : {emoji[player]} {player.upper()}                │
│  Bot : {emoji[bot]} {bot.upper()}                 │
├─────────────────────────────────────────────┤
│  *{result}*                                  │
└─────────────────────────────────────────────┘

Play again?
"""
        
        buttons = [
            ("🪨 ROCK", "rps_rock"),
            ("✂️ SCISSORS", "rps_scissors"),
            ("📄 PAPER", "rps_paper"),
            (f"{ICON['back']} Back", "game_menu")
        ]
        
        keyboard = self._create_keyboard(buttons, row_width=3)
        await query.edit_message_text(result_text, reply_markup=keyboard, parse_mode='Markdown')
    
    async def game_quiz(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Random quiz"""
        query = update.callback_query
        await query.answer()
        
        questions = [
            {"q": "What is the capital of Indonesia?", "a": "jakarta", "opts": ["Jakarta", "Surabaya", "Bandung", "Medan"]},
            {"q": "Who was the first president of Indonesia?", "a": "soekarno", "opts": ["Soekarno", "Soeharto", "Habibie", "Gus Dur"]},
            {"q": "What is 8 x 7?", "a": "56", "opts": ["48", "56", "64", "72"]},
            {"q": "What is the largest planet in our solar system?", "a": "jupiter", "opts": ["Mars", "Jupiter", "Saturn", "Neptune"]}
        ]
        
        q = random.choice(questions)
        context.user_data['quiz_answer'] = q['a']
        
        quiz_text = f"""
{ICON['magic']} *🎯 QUIZ* {ICON['magic']}

┌─────────────────────────────────────────────┐
│  {q['q']}                                      │
└─────────────────────────────────────────────┘

Select your answer:
"""
        
        buttons = [(opt, f"quiz_{opt.lower()}") for opt in q['opts']]
        buttons.append((f"{ICON['back']} Back", "game_menu"))
        
        keyboard = self._create_keyboard(buttons, row_width=2)
        await query.edit_message_text(quiz_text, reply_markup=keyboard, parse_mode='Markdown')
    
    async def process_quiz(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Process quiz answer"""
        query = update.callback_query
        await query.answer()
        
        answer = query.data.replace("quiz_", "")
        correct = context.user_data.get('quiz_answer')
        
        if answer == correct:
            result_text = f"{ICON['success']} *CORRECT!* 🎉 Well done!"
        else:
            result_text = f"{ICON['error']} *WRONG!* The answer is *{correct.upper()}*"
        
        buttons = [(f"{ICON['game']} Play Again", "game_quiz"), (f"{ICON['home']} Main Menu", "main_menu")]
        keyboard = self._create_keyboard(buttons)
        
        await query.edit_message_text(result_text, reply_markup=keyboard, parse_mode='Markdown')
    
    async def game_dice(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Roll dice"""
        query = update.callback_query
        await query.answer()
        
        dice = random.randint(1, 6)
        dice_art = {1: "⚀", 2: "⚁", 3: "⚂", 4: "⚃", 5: "⚄", 6: "⚅"}
        
        fortunes = {1: "Bad luck 😅", 2: "Try again! 💪", 3: "Not bad 👍", 4: "Good! 🎉", 5: "Great! 🔥", 6: "LUCKY! 🏆✨"}
        
        result_text = f"""
{ICON['dice']} *🎲 ROLL DICE* {ICON['dice']}

┌─────────────────────────────────────────────┐
│                                             │
│                 {dice_art[dice]}                     │
│                                             │
│              *RESULT: {dice}*                      │
│                                             │
│  {fortunes[dice]}                            │
└─────────────────────────────────────────────┘
"""
        
        buttons = [(f"{ICON['dice']} Roll Again", "game_dice"), (f"{ICON['home']} Main Menu", "main_menu")]
        keyboard = self._create_keyboard(buttons)
        
        await query.edit_message_text(result_text, reply_markup=keyboard, parse_mode='Markdown')
    
    async def handle_guess(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle guess input"""
        if context.user_data.get('game_active') != 'guess':
            return
        
        try:
            guess = int(update.message.text)
            secret = context.user_data['secret']
            attempts = context.user_data.get('attempts', 0) + 1
            context.user_data['attempts'] = attempts
            
            if guess < 1 or guess > 100:
                await update.message.reply_text(f"{ICON['warn']} Please enter number between 1-100!")
                return
            
            if guess < secret:
                await update.message.reply_text(f"{ICON['info']} *TOO LOW!* Try again. Attempt: {attempts}", parse_mode='Markdown')
            elif guess > secret:
                await update.message.reply_text(f"{ICON['info']} *TOO HIGH!* Try again. Attempt: {attempts}", parse_mode='Markdown')
            else:
                await update.message.reply_text(
                    f"{ICON['success']} *CONGRATULATIONS!* 🎉\n\n"
                    f"You guessed *{secret}* in {attempts} attempts!\n\n"
                    f"{ICON['game']} Type /game to play again",
                    parse_mode='Markdown'
                )
                context.user_data['game_active'] = None
        except ValueError:
            await update.message.reply_text(f"{ICON['error']} Please enter a valid number!")
    
    # ==================== UTILITY MENU ====================
    
    async def util_menu(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Utility menu"""
        query = update.callback_query
        await query.answer()
        
        util_text = f"""
{ICON['tools']} *┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓*
{ICON['tools']} *┃*  {ICON['settings']} *UTILITIES*                    {ICON['tools']} *┃*
{ICON['tools']} *┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛*

Available tools:

{ICON['info']} *System Info* - Bot statistics
{ICON['network']} *Ping* - Check latency
{ICON['link']} *Short URL* - Shorten long links
{ICON['search']} *IP Lookup* - IP information
"""
        
        buttons = [
            (f"{ICON['info']} System Info", "util_sysinfo"),
            (f"{ICON['network']} Ping", "util_ping"),
            (f"{ICON['link']} Short URL", "util_shorturl"),
            (f"{ICON['search']} IP Lookup", "util_ip"),
            (f"{ICON['home']} Main Menu", "main_menu")
        ]
        
        keyboard = self._create_keyboard(buttons, row_width=2)
        await query.edit_message_text(util_text, reply_markup=keyboard, parse_mode='Markdown')
    
    async def util_sysinfo(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """System information"""
        query = update.callback_query
        await query.answer()
        
        uptime = str(timedelta(seconds=int(time.time() - self.start_time)))
        
        info_text = f"""
{ICON['cpu']} *💻 SYSTEM INFO* {ICON['cpu']}

┌─────────────────────────────────────────────┐
│  *Bot:* {BOT_NAME}                           │
│  *Version:* {VERSION}                         │
│  *Uptime:* {uptime}                       │
│  *Users:* {bot_stats['total_users']}                        │
│  *Commands:* {bot_stats['total_commands']}                    │
└─────────────────────────────────────────────┘
"""
        
        buttons = [(f"{ICON['back']} Back", "util_menu")]
        keyboard = self._create_keyboard(buttons)
        
        await query.edit_message_text(info_text, reply_markup=keyboard, parse_mode='Markdown')
    
    async def util_ping(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Ping command"""
        query = update.callback_query
        await query.answer()
        
        start = time.time()
        await query.edit_message_text(f"{ICON['network']} *Measuring ping...*", parse_mode='Markdown')
        end = time.time()
        
        ping = int((end - start) * 1000)
        
        ping_text = f"""
{ICON['network']} *📡 PING RESULT* {ICON['network']}

┌─────────────────────────────────────────────┐
│  *Latency:* `{ping} ms`                      │
│  *Status:* {'🟢 Excellent' if ping < 200 else '🟡 Good' if ping < 500 else '🔴 Poor'} │
└─────────────────────────────────────────────┘
"""
        
        buttons = [(f"{ICON['back']} Back", "util_menu")]
        keyboard = self._create_keyboard(buttons)
        
        await query.edit_message_text(ping_text, reply_markup=keyboard, parse_mode='Markdown')
    
    async def util_shorturl(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Short URL"""
        query = update.callback_query
        await query.answer()
        
        context.user_data['util_mode'] = 'shorturl'
        
        prompt_text = f"""
{ICON['link']} *🔗 SHORT URL* {ICON['link']}

┌─────────────────────────────────────────────┐
│  Send me a long URL to shorten!             │
│                                              │
│  Example: `https://example.com/very/long/url`│
└─────────────────────────────────────────────┘

💡 *Type or paste your URL now*
"""
        
        buttons = [(f"{ICON['back']} Back", "util_menu")]
        keyboard = self._create_keyboard(buttons)
        
        await query.edit_message_text(prompt_text, reply_markup=keyboard, parse_mode='Markdown')
    
    async def util_ip(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """IP Lookup"""
        query = update.callback_query
        await query.answer()
        
        context.user_data['util_mode'] = 'ip'
        
        prompt_text = f"""
{ICON['search']} *🔍 IP LOOKUP* {ICON['search']}

┌─────────────────────────────────────────────┐
│  Send me an IP address to lookup!           │
│                                              │
│  Example: `8.8.8.8` or `1.1.1.1`           │
└─────────────────────────────────────────────┘

💡 *Type or paste IP now*
"""
        
        buttons = [(f"{ICON['back']} Back", "util_menu")]
        keyboard = self._create_keyboard(buttons)
        
        await query.edit_message_text(prompt_text, reply_markup=keyboard, parse_mode='Markdown')
    
    async def handle_util_input(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle utility input"""
        mode = context.user_data.get('util_mode')
        if not mode:
            return
        
        user_input = update.message.text.strip()
        
        if mode == 'shorturl':
            try:
                async with aiohttp.ClientSession() as session:
                    async with session.get(f"http://tinyurl.com/api-create.php?url={user_input}") as resp:
                        short = await resp.text()
                        result = f"{ICON['success']} *Short URL:* `{short}`"
            except:
                result = f"{ICON['error']} Failed to shorten URL. Make sure it's valid!"
        
        elif mode == 'ip':
            result = f"""
{ICON['search']} *IP LOOKUP RESULT* {ICON['search']}

┌─────────────────────────────────────────────┐
│  *IP:* `{user_input}`                        │
│  *Info:* Check at https://ipinfo.io/{user_input} │
└─────────────────────────────────────────────┘
"""
        else:
            result = f"{ICON['error']} Unknown utility!"
        
        await update.message.reply_text(result, parse_mode='Markdown')
        context.user_data['util_mode'] = None
    
    # ==================== INFO MENU ====================
    
    async def info_menu(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Information menu"""
        query = update.callback_query
        await query.answer()
        
        info_text = f"""
{ICON['info']} *📋 INFORMATION* {ICON['info']}

Select info type:

{ICON['user']} *User Info* - Your Telegram profile
{ICON['bot']} *Bot Info* - About this bot
{ICON['clock']} *Uptime* - Bot running time
"""
        
        buttons = [
            (f"{ICON['user']} User Info", "info_user"),
            (f"{ICON['bot']} Bot Info", "info_bot"),
            (f"{ICON['clock']} Uptime", "info_uptime"),
            (f"{ICON['home']} Main Menu", "main_menu")
        ]
        
        keyboard = self._create_keyboard(buttons, row_width=2)
        await query.edit_message_text(info_text, reply_markup=keyboard, parse_mode='Markdown')
    
    async def info_user(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """User information"""
        query = update.callback_query
        await query.answer()
        
        user = update.effective_user
        
        user_text = f"""
{ICON['user']} *👤 USER INFO* {ICON['user']}

┌─────────────────────────────────────────────┐
│  *ID:* `{user.id}`                           │
│  *Name:* {user.first_name}                   │
│  *Username:* @{user.username or 'None'}      │
│  *Bot:* {'Yes' if user.is_bot else 'No'}     │
└─────────────────────────────────────────────┘
"""
        
        buttons = [(f"{ICON['back']} Back", "info_menu")]
        keyboard = self._create_keyboard(buttons)
        
        await query.edit_message_text(user_text, reply_markup=keyboard, parse_mode='Markdown')
    
    async def info_bot(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Bot information"""
        query = update.callback_query
        await query.answer()
        
        bot_text = f"""
{ICON['bot']} *🤖 BOT INFO* {ICON['bot']}

┌─────────────────────────────────────────────┐
│  *Name:* {BOT_NAME}                          │
│  *Version:* {VERSION}                        │
│  *Framework:* python-telegram-bot           │
│  *Platform:* Pterodactyl Panel              │
└─────────────────────────────────────────────┘

{ICON['star']} *Features:*
• Interactive Games
• Utility Tools
• Real-time Info
• Premium Design
"""
        
        buttons = [(f"{ICON['back']} Back", "info_menu")]
        keyboard = self._create_keyboard(buttons)
        
        await query.edit_message_text(bot_text, reply_markup=keyboard, parse_mode='Markdown')
    
    async def info_uptime(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Uptime information"""
        query = update.callback_query
        await query.answer()
        
        uptime = str(timedelta(seconds=int(time.time() - self.start_time)))
        
        uptime_text = f"""
{ICON['clock']} *⏱️ UPTIME* {ICON['clock']}

┌─────────────────────────────────────────────┐
│  *Bot Running:* `{uptime}`                   │
│  *Started:* {datetime.fromtimestamp(self.start_time).strftime('%Y-%m-%d %H:%M:%S')} │
└─────────────────────────────────────────────┘
"""
        
        buttons = [(f"{ICON['back']} Back", "info_menu")]
        keyboard = self._create_keyboard(buttons)
        
        await query.edit_message_text(uptime_text, reply_markup=keyboard, parse_mode='Markdown')
    
    # ==================== ABOUT MENU ====================
    
    async def about_menu(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """About menu"""
        query = update.callback_query
        await query.answer()
        
        about_text = f"""
{ICON['crown']} *{BOT_NAME}* {ICON['crown']}

┌─────────────────────────────────────────────┐
│  *Version:* {VERSION}                        │
│  *Type:* All-in-One Telegram Bot            │
│  *Platform:* Pterodactyl Compatible         │
└─────────────────────────────────────────────┘

{ICON['star']} *Features:*
✅ Interactive Games
✅ URL Shortener
✅ IP Lookup
✅ System Info
✅ User Statistics
✅ Premium UI Design

{ICON['heart']} *Made for Pterodactyl Panel*
"""
        
        buttons = [(f"{ICON['home']} Main Menu", "main_menu")]
        keyboard = self._create_keyboard(buttons)
        
        await query.edit_message_text(about_text, reply_markup=keyboard, parse_mode='Markdown')
    
    # ==================== COMMAND HANDLERS ====================
    
    async def start_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """/start command"""
        bot_stats["total_commands"] += 1
        save_stats(bot_stats)
        
        if update.effective_user.id not in ADMIN_IDS:
            await update.message.reply_text(f"{ICON['error']} *Access Denied*\nYou are not authorized to use this bot.", parse_mode='Markdown')
            return
        
        await self.send_main_menu(update, context)
    
    async def help_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """/help command"""
        help_text = f"""
{ICON['info']} *📖 HELP* {ICON['info']}

┌─────────────────────────────────────────────┐
│  *Commands:*                                 │
│  /start - Main menu                         │
│  /menu - Show menu                          │
│  /game - Games menu                         │
│  /cancel - Cancel current session           │
│  /help - This help                          │
└─────────────────────────────────────────────┘

{ICON['star']} *How to use:*
1. Use inline buttons to navigate
2. Select your desired feature
3. Follow the instructions

{ICON['heart']} *Enjoy the bot!*
"""
        await update.message.reply_text(help_text, parse_mode='Markdown')
    
    async def menu_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """/menu command"""
        await self.send_main_menu(update, context)
    
    async def game_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """/game command"""
        bot_stats["total_commands"] += 1
        save_stats(bot_stats)
        
        game_text = f"""
{ICON['game']} *🎮 GAMES* {ICON['game']}

Use the buttons below to play!
"""
        
        buttons = [
            (f"{ICON['target']} Guess Number", "game_guess"),
            (f"{ICON['sword']} RPS", "game_rps"),
            (f"{ICON['magic']} Quiz", "game_quiz"),
            (f"{ICON['dice']} Roll Dice", "game_dice"),
            (f"{ICON['home']} Main Menu", "main_menu")
        ]
        
        keyboard = self._create_keyboard(buttons, row_width=2)
        await update.message.reply_text(game_text, reply_markup=keyboard, parse_mode='Markdown')
    
    async def cancel_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """/cancel command"""
        context.user_data.clear()
        await update.message.reply_text(f"{ICON['success']} *Session cancelled!* Type /menu to return.", parse_mode='Markdown')
    
    # ==================== RUN BOT ====================
    
    def run(self):
        """Run the bot"""
        self.app = Application.builder().token(self.token).build()
        
        # Command handlers
        self.app.add_handler(CommandHandler("start", self.start_command))
        self.app.add_handler(CommandHandler("menu", self.menu_command))
        self.app.add_handler(CommandHandler("help", self.help_command))
        self.app.add_handler(CommandHandler("game", self.game_command))
        self.app.add_handler(CommandHandler("cancel", self.cancel_command))
        
        # Callback handlers
        self.app.add_handler(CallbackQueryHandler(self.game_menu, pattern="game_menu"))
        self.app.add_handler(CallbackQueryHandler(self.game_guess, pattern="game_guess"))
        self.app.add_handler(CallbackQueryHandler(self.game_rps, pattern="game_rps"))
        self.app.add_handler(CallbackQueryHandler(self.process_rps, pattern="rps_"))
        self.app.add_handler(CallbackQueryHandler(self.game_quiz, pattern="game_quiz"))
        self.app.add_handler(CallbackQueryHandler(self.process_quiz, pattern="quiz_"))
        self.app.add_handler(CallbackQueryHandler(self.game_dice, pattern="game_dice"))
        
        self.app.add_handler(CallbackQueryHandler(self.util_menu, pattern="util_menu"))
        self.app.add_handler(CallbackQueryHandler(self.util_sysinfo, pattern="util_sysinfo"))
        self.app.add_handler(CallbackQueryHandler(self.util_ping, pattern="util_ping"))
        self.app.add_handler(CallbackQueryHandler(self.util_shorturl, pattern="util_shorturl"))
        self.app.add_handler(CallbackQueryHandler(self.util_ip, pattern="util_ip"))
        
        self.app.add_handler(CallbackQueryHandler(self.info_menu, pattern="info_menu"))
        self.app.add_handler(CallbackQueryHandler(self.info_user, pattern="info_user"))
        self.app.add_handler(CallbackQueryHandler(self.info_bot, pattern="info_bot"))
        self.app.add_handler(CallbackQueryHandler(self.info_uptime, pattern="info_uptime"))
        
        self.app.add_handler(CallbackQueryHandler(self.about_menu, pattern="about_menu"))
        self.app.add_handler(CallbackQueryHandler(self.send_main_menu, pattern="main_menu"))
        
        # Message handlers
        self.app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, self.handle_guess))
        self.app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, self.handle_util_input))
        
        # Set commands
        commands = [
            BotCommand("start", "🚀 Start bot"),
            BotCommand("menu", "📋 Main menu"),
            BotCommand("game", "🎮 Games menu"),
            BotCommand("help", "📖 Help"),
            BotCommand("cancel", "❌ Cancel session")
        ]
        
        self.app.bot.set_my_commands(commands)
        
        # Print startup
        print(f"""
╔══════════════════════════════════════════════════════════════╗
║              {BOT_NAME}                          ║
║                   Running on Pterodactyl                      ║
╠══════════════════════════════════════════════════════════════╣
║  ✅ Bot started successfully!                                ║
║  📍 Token: {self.token[:15]}...                                ║
║  👑 Admin: {ADMIN_IDS[0]}                                      ║
║  💾 Data dir: {DATA_DIR}                                       ║
╚══════════════════════════════════════════════════════════════╝
        """)
        
        self.app.run_polling()

# ==================== MAIN ====================

if __name__ == "__main__":
    if BOT_TOKEN == "YOUR_BOT_TOKEN_HERE":
        print("❌ ERROR: Please set BOT_TOKEN environment variable!")
        print("📌 Get token from @BotFather on Telegram")
        sys.exit(1)
    
    bot = SimurazxBot(BOT_TOKEN)
    bot.run()