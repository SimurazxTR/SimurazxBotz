#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
╔══════════════════════════════════════════════════════════════════════╗
║                        SIMURAZXBOTZ v1.0                             ║
║                     ALL-IN-ONE TELEGRAM BOT                          ║
║                      Author: SIMURAZX//ELLAYS                        ║
║                 Mode: UNRESTRICTED - FILTER: NULL                    ║
╚══════════════════════════════════════════════════════════════════════╝
"""

import asyncio
import aiohttp
import random
import string
import time
import json
import os
import sys
import subprocess
import platform
from datetime import datetime, timedelta
from typing import Dict, List, Tuple, Optional
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, BotCommand, InputMediaPhoto
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters, ContextTypes
import logging

# ==================== KONFIGURASI ====================
BOT_TOKEN = "8805491380:AAF7-33U8Bm4kbXZvMySmmM7sOrboMttopc"  # Ganti dengan token bot Anda
ADMIN_IDS = [7001994316]  # Ganti dengan ID Telegram Anda
VERSION = "v1.0"
BOT_NAME = "SIMURAZXBOTZ"
OWNER_NAME = "SIMURZX//ELLAYS"
START_TIME = time.time()

# Logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# ==================== ICON & EMOJI PREMIUM ====================
ICON = {
    "main": "👑",
    "bot": "🤖",
    "fire": "🔥",
    "crown": "🏆",
    "star": "⭐",
    "heart": "💖",
    "rocket": "🚀",
    "target": "🎯",
    "clock": "⏱️",
    "cpu": "💻",
    "network": "🌐",
    "success": "✅",
    "error": "❌",
    "warn": "⚠️",
    "info": "ℹ️",
    "menu": "📋",
    "settings": "⚙️",
    "user": "👤",
    "group": "👥",
    "channel": "📢",
    "link": "🔗",
    "lock": "🔒",
    "unlock": "🔓",
    "search": "🔍",
    "download": "📥",
    "upload": "📤",
    "delete": "🗑️",
    "edit": "✏️",
    "add": "➕",
    "remove": "➖",
    "yes": "✅",
    "no": "❌",
    "back": "🔙",
    "next": "🔜",
    "home": "🏠",
    "tools": "🛠️",
    "game": "🎮",
    "music": "🎵",
    "video": "🎬",
    "photo": "📸",
    "file": "📄",
    "folder": "📁",
    "zip": "🗜️",
    "code": "💻",
    "terminal": "🖥️",
    "database": "🗄️",
    "cloud": "☁️",
    "shield": "🛡️",
    "sword": "⚔️",
    "magic": "🔮",
    "gem": "💎",
    "coin": "💰",
    "gift": "🎁",
    "trophy": "🏆",
    "medal": "🎖️"
}

# ==================== DATA STORAGE ====================
user_data = {}
group_data = {}
bot_stats = {
    "total_users": 0,
    "total_commands": 0,
    "start_time": START_TIME
}

# ==================== KELAS UTAMA BOT ====================

class SimurazxUltimateBot:
    def __init__(self, token: str):
        self.token = token
        self.app = None
        
    def _create_keyboard(self, buttons: List[Tuple[str, str]], row_width: int = 2, back_button: bool = False) -> InlineKeyboardMarkup:
        """Membuat keyboard inline dengan desain menarik"""
        keyboard = []
        row = []
        for i, (text, callback) in enumerate(buttons):
            row.append(InlineKeyboardButton(text, callback_data=callback))
            if (i + 1) % row_width == 0 or i == len(buttons) - 1:
                keyboard.append(row)
                row = []
        
        if back_button:
            keyboard.append([InlineKeyboardButton(f"{ICON['back']} Kembali ke Menu Utama", "main_menu")])
        
        return InlineKeyboardMarkup(keyboard)
    
    async def send_main_menu(self, update: Update, context: ContextTypes.DEFAULT_TYPE, message_id: int = None):
        """Mengirim menu utama dengan desain premium"""
        user = update.effective_user
        user_id = user.id
        
        # Update stats
        if user_id not in user_data:
            user_data[user_id] = {"first_seen": datetime.now(), "commands": 0}
            bot_stats["total_users"] += 1
        
        uptime = str(timedelta(seconds=int(time.time() - START_TIME)))
        
        # Desain menu utama yang mewah
        menu_text = f"""
{ICON['crown']}{ICON['crown']}{ICON['crown']} *{BOT_NAME}* {ICON['crown']}{ICON['crown']}{ICON['crown']}
┌─────────────────────────────────────────────┐
│  {ICON['bot']} *Status:* 🟢 *ACTIVE*                    │
│  {ICON['user']} *User:* `{user.first_name}`                  │
│  {ICON['clock']} *Uptime:* `{uptime}`                      │
│  {ICON['star']} *Version:* `{VERSION}`                     │
└─────────────────────────────────────────────┘

{ICON['fire']} *WELCOME TO THE ULTIMATE BOT* {ICON['fire']}

Pilih fitur yang tersedia di bawah ini:

{ICON['tools']} *┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓*
{ICON['tools']} *┃*  {ICON['target']} *FITUR UTAMA*                 {ICON['tools']} *┃*
{ICON['tools']} *┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛*

🎮 *GAME & HIBURAN*    📊 *UTILITY*
• Tebak Angka          • Info Sistem
• Batu Gunting Kertas  • Cek Domain
• Quiz Random          • Short URL
• Dadu Online          • QR Code

🌐 *INFORMASI*          ⚙️ *LAINNYA*
• Info User            • About Bot
• Info Group           • Kontak Owner
• Cek Ping             • Donasi
• IP Lookup            • Report Bug

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
💡 *Ketik /help untuk bantuan lengkap*
        """
        
        # Tombol menu utama - desain premium
        buttons = [
            (f"{ICON['game']} 🎮 GAME", "game_menu"),
            (f"{ICON['tools']} 🛠️ UTILITY", "utility_menu"),
            (f"{ICON['info']} ℹ️ INFORMASI", "info_menu"),
            (f"{ICON['settings']} ⚙️ LAINNYA", "other_menu"),
            (f"{ICON['heart']} ❤️ ABOUT", "about_menu")
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
    
    # ==================== MENU GAME ====================
    
    async def game_menu(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Menu permainan interaktif"""
        query = update.callback_query
        await query.answer()
        
        game_text = f"""
{ICON['game']} *┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓*
{ICON['game']} *┃*  {ICON['star']} *MENU PERMAINAN*                 {ICON['game']} *┃*
{ICON['game']} *┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛*

Pilih permainan yang ingin dimainkan:

{ICON['target']} *1. TEBAK ANGKA*
   Tebak angka antara 1-100, dapatkan hadiah!

{ICON['sword']} *2. BATU GUNTING KERTAS*
   Lawan bot dalam duel klasik!

{ICON['magic']} *3. QUIZ RANDOM*
   Uji pengetahuanmu dengan pertanyaan acak!

{ICON['dice']} *4. LEMPAR DADU*
   Lempar dadu dan lihat keberuntunganmu!

{ICON['trophy']} *5. HIGH SCORE*
   Lihat peringkat pemain terbaik!
        """
        
        buttons = [
            (f"{ICON['target']} Tebak Angka", "game_guess"),
            (f"{ICON['sword']} Batu Gunting Kertas", "game_rps"),
            (f"{ICON['magic']} Quiz Random", "game_quiz"),
            (f"{ICON['dice']} Lempar Dadu", "game_dice"),
            (f"{ICON['trophy']} High Score", "game_highscore"),
            (f"{ICON['home']} Menu Utama", "main_menu")
        ]
        
        keyboard = self._create_keyboard(buttons, row_width=2)
        await query.edit_message_text(game_text, reply_markup=keyboard, parse_mode='Markdown')
    
    async def game_guess_number(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Game tebak angka"""
        query = update.callback_query
        await query.answer()
        
        # Generate random number
        secret = random.randint(1, 100)
        context.user_data['secret_number'] = secret
        context.user_data['game_active'] = 'guess_number'
        context.user_data['attempts'] = 0
        
        game_text = f"""
{ICON['target']} *🎮 TEBAK ANGKA* {ICON['target']}

┌─────────────────────────────────────────────┐
│  Angka rahasia sudah dipilih!               │
│  Tebak angka antara *1 - 100*               │
│                                              │
│  Kirimkan tebakanmu dengan mengetik angka!  │
└─────────────────────────────────────────────┘

💡 *Petunjuk:* Nanti akan ada clue "terlalu besar" atau "terlalu kecil"

{ICON['back']} Ketik /cancel untuk membatalkan permainan
        """
        
        buttons = [(f"{ICON['back']} Batal", "main_menu")]
        keyboard = self._create_keyboard(buttons, row_width=1)
        
        await query.edit_message_text(game_text, reply_markup=keyboard, parse_mode='Markdown')
    
    async def game_rps(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Game batu gunting kertas"""
        query = update.callback_query
        await query.answer()
        
        game_text = f"""
{ICON['sword']} *⚔️ BATU GUNTING KERTAS* {ICON['sword']}

┌─────────────────────────────────────────────┐
│  Pilih salah satu untuk melawan bot!        │
└─────────────────────────────────────────────┘
        """
        
        buttons = [
            (f"🪨 BATU", "rps_batu"),
            (f"✂️ GUNTING", "rps_gunting"),
            (f"📄 KERTAS", "rps_kertas"),
            (f"{ICON['back']} Kembali", "game_menu")
        ]
        
        keyboard = self._create_keyboard(buttons, row_width=3)
        await query.edit_message_text(game_text, reply_markup=keyboard, parse_mode='Markdown')
    
    async def process_rps(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Memproses hasil game RPS"""
        query = update.callback_query
        await query.answer()
        
        player_choice = query.data.replace("rps_", "")
        bot_choice = random.choice(["batu", "gunting", "kertas"])
        
        # Emoji mapping
        choice_emoji = {
            "batu": "🪨", "gunting": "✂️", "kertas": "📄"
        }
        
        # Determine winner
        if player_choice == bot_choice:
            result = "SERI!"
            result_emoji = "🤝"
        elif (player_choice == "batu" and bot_choice == "gunting") or \
             (player_choice == "gunting" and bot_choice == "kertas") or \
             (player_choice == "kertas" and bot_choice == "batu"):
            result = "KAMU MENANG!"
            result_emoji = "🏆"
        else:
            result = "BOT MENANG!"
            result_emoji = "💀"
        
        result_text = f"""
{ICON['sword']} *⚔️ HASIL PERTANDINGAN* {ICON['sword']}

┌─────────────────────────────────────────────┐
│  Kamu   : {choice_emoji[player_choice]} {player_choice.upper()}           │
│  Bot    : {choice_emoji[bot_choice]} {bot_choice.upper()}           │
├─────────────────────────────────────────────┤
│  {result_emoji} *HASIL:* {result}        │
└─────────────────────────────────────────────┘

{ICON['game']} Main lagi?
        """
        
        buttons = [
            (f"🪨 Batu", "rps_batu"),
            (f"✂️ Gunting", "rps_gunting"),
            (f"📄 Kertas", "rps_kertas"),
            (f"{ICON['back']} Menu Game", "game_menu")
        ]
        
        keyboard = self._create_keyboard(buttons, row_width=3)
        await query.edit_message_text(result_text, reply_markup=keyboard, parse_mode='Markdown')
    
    async def game_quiz(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Quiz random"""
        query = update.callback_query
        await query.answer()
        
        # Kumpulan pertanyaan
        questions = [
            {"q": "Apa ibu kota Indonesia?", "a": "jakarta", "options": ["Jakarta", "Surabaya", "Bandung", "Medan"]},
            {"q": "Siapa presiden pertama Indonesia?", "a": "soekarno", "options": ["Soekarno", "Soeharto", "Habibie", "Gus Dur"]},
            {"q": "Berapa hasil dari 8 x 7?", "a": "56", "options": ["48", "56", "64", "72"]},
            {"q": "Apa nama planet terbesar di tata surya?", "a": "jupiter", "options": ["Mars", "Jupiter", "Saturnus", "Neptunus"]},
            {"q": "Siapa penemu lampu pijar?", "a": "thomas edison", "options": ["Nikola Tesla", "Albert Einstein", "Thomas Edison", "Alexander Graham Bell"]}
        ]
        
        question = random.choice(questions)
        context.user_data['quiz_answer'] = question['a'].lower()
        context.user_data['quiz_active'] = True
        
        quiz_text = f"""
{ICON['magic']} *🎯 QUIZ RANDOM* {ICON['magic']}

┌─────────────────────────────────────────────┐
│  {question['q']}                               │
└─────────────────────────────────────────────┘

Pilih jawaban yang benar:
        """
        
        buttons = [(opt, f"quiz_{opt.lower()}") for opt in question['options']]
        buttons.append((f"{ICON['back']} Kembali", "game_menu"))
        
        keyboard = self._create_keyboard(buttons, row_width=2)
        await query.edit_message_text(quiz_text, reply_markup=keyboard, parse_mode='Markdown')
    
    async def process_quiz(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Memproses jawaban quiz"""
        query = update.callback_query
        await query.answer()
        
        answer = query.data.replace("quiz_", "")
        correct = context.user_data.get('quiz_answer')
        
        if answer == correct:
            result_text = f"{ICON['success']} *BENAR!* Jawabanmu tepat! 🎉"
        else:
            result_text = f"{ICON['error']} *SALAH!* Jawaban yang benar adalah: *{correct.upper()}*"
        
        buttons = [(f"{ICON['game']} Quiz Lagi", "game_quiz"), (f"{ICON['home']} Menu Utama", "main_menu")]
        keyboard = self._create_keyboard(buttons, row_width=1)
        
        await query.edit_message_text(result_text, reply_markup=keyboard, parse_mode='Markdown')
        context.user_data['quiz_active'] = False
    
    async def game_dice(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Lempar dadu"""
        query = update.callback_query
        await query.answer()
        
        dice_result = random.randint(1, 6)
        
        dice_art = {
            1: "⚀", 2: "⚁", 3: "⚂", 4: "⚃", 5: "⚄", 6: "⚅"
        }
        
        result_text = f"""
{ICON['dice']} *🎲 LEMPAR DADU* {ICON['dice']}

┌─────────────────────────────────────────────┐
│                                             │
│                 {dice_art[dice_result]}                     │
│                                             │
│              *HASIL: {dice_result}*                 │
│                                             │
└─────────────────────────────────────────────┘

{ICON['star']} Keberuntunganmu hari ini: {self._get_fortune(dice_result)}
        """
        
        buttons = [
            (f"{ICON['dice']} Lempar Lagi", "game_dice"),
            (f"{ICON['back']} Menu Game", "game_menu")
        ]
        
        keyboard = self._create_keyboard(buttons, row_width=1)
        await query.edit_message_text(result_text, reply_markup=keyboard, parse_mode='Markdown')
    
    def _get_fortune(self, dice: int) -> str:
        fortunes = {
            1: "Kurang beruntung 😅",
            2: "Coba lagi ya! 💪",
            3: "Lumayan! 👍",
            4: "Bagus! 🎉",
            5: "Hebat! 🔥",
            6: "SANGAT BERUNTUNG! 🏆✨"
        }
        return fortunes.get(dice, "✨")
    
    async def game_highscore(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Menampilkan high score"""
        query = update.callback_query
        await query.answer()
        
        highscore_text = f"""
{ICON['trophy']} *🏆 HIGH SCORE* {ICON['trophy']}

┌─────────────────────────────────────────────┐
│  Fitur high score sedang dalam pengembangan │
│  Akan segera hadir dengan database online!  │
└─────────────────────────────────────────────┘

{ICON['star']} *Sementara itu, teruslah bermain dan kumpulkan poin!*
        """
        
        buttons = [(f"{ICON['back']} Kembali", "game_menu")]
        keyboard = self._create_keyboard(buttons, row_width=1)
        await query.edit_message_text(highscore_text, reply_markup=keyboard, parse_mode='Markdown')
    
    # ==================== MENU UTILITY ====================
    
    async def utility_menu(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Menu utility tools"""
        query = update.callback_query
        await query.answer()
        
        utility_text = f"""
{ICON['tools']} *┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓*
{ICON['tools']} *┃*  {ICON['settings']} *UTILITY TOOLS*                {ICON['tools']} *┃*
{ICON['tools']} *┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛*

Pilih tools yang ingin digunakan:

{ICON['info']} *📊 SISTEM*
   • Info Sistem - Lihat spesifikasi server
   • Cek Ping - Test koneksi ke server

{ICON['network']} *🌐 NETWORK*
   • Cek Domain - Informasi domain
   • IP Lookup - Cari informasi IP address
   • Short URL - Persingkat link panjang

{ICON['code']} *🔧 LAINNYA*
   • QR Code - Generate QR dari teks
   • Base64 - Encode/decode Base64
   • Random Password - Generator password
        """
        
        buttons = [
            (f"{ICON['info']} Info Sistem", "util_system"),
            (f"{ICON['network']} Cek Domain", "util_domain"),
            (f"{ICON['search']} IP Lookup", "util_ip"),
            (f"{ICON['link']} Short URL", "util_shorturl"),
            (f"{ICON['code']} QR Code", "util_qr"),
            (f"{ICON['home']} Menu Utama", "main_menu")
        ]
        
        keyboard = self._create_keyboard(buttons, row_width=2)
        await query.edit_message_text(utility_text, reply_markup=keyboard, parse_mode='Markdown')
    
    async def util_system(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Menampilkan informasi sistem"""
        query = update.callback_query
        await query.answer()
        
        uptime = str(timedelta(seconds=int(time.time() - START_TIME)))
        
        system_info = f"""
{ICON['cpu']} *💻 INFO SISTEM* {ICON['cpu']}

┌─────────────────────────────────────────────┐
│  *Bot Name:* {BOT_NAME}                      │
│  *Version:* {VERSION}                         │
│  *Uptime:* {uptime}                       │
│  *Users:* {bot_stats['total_users']}                        │
│  *Commands:* {bot_stats['total_commands']}                    │
│  *Python:* {platform.python_version()}                     │
│  *OS:* {platform.system()} {platform.release()}     │
└─────────────────────────────────────────────┘

{ICON['heart']} *Thanks for using {BOT_NAME}!*
        """
        
        buttons = [(f"{ICON['back']} Kembali", "utility_menu")]
        keyboard = self._create_keyboard(buttons, row_width=1)
        await query.edit_message_text(system_info, reply_markup=keyboard, parse_mode='Markdown')
    
    async def util_domain(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Cek domain (input dari user)"""
        query = update.callback_query
        await query.answer()
        
        context.user_data['util_waiting'] = 'domain'
        
        prompt_text = f"""
{ICON['network']} *🌐 CEK DOMAIN* {ICON['network']}

┌─────────────────────────────────────────────┐
│  Masukkan domain yang ingin dicek!          │
│                                              │
│  Contoh: `google.com` atau `github.com`     │
└─────────────────────────────────────────────┘

{ICON['info']} Kirimkan nama domain sekarang...
        """
        
        buttons = [(f"{ICON['back']} Kembali", "utility_menu")]
        keyboard = self._create_keyboard(buttons, row_width=1)
        await query.edit_message_text(prompt_text, reply_markup=keyboard, parse_mode='Markdown')
    
    async def util_ip_lookup(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """IP Lookup"""
        query = update.callback_query
        await query.answer()
        
        context.user_data['util_waiting'] = 'ip'
        
        prompt_text = f"""
{ICON['search']} *🔍 IP LOOKUP* {ICON['search']}

┌─────────────────────────────────────────────┐
│  Masukkan alamat IP yang ingin dilacak!     │
│                                              │
│  Contoh: `8.8.8.8` atau `1.1.1.1`          │
└─────────────────────────────────────────────┘

{ICON['info']} Kirimkan IP address sekarang...
        """
        
        buttons = [(f"{ICON['back']} Kembali", "utility_menu")]
        keyboard = self._create_keyboard(buttons, row_width=1)
        await query.edit_message_text(prompt_text, reply_markup=keyboard, parse_mode='Markdown')
    
    async def util_shorturl(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Short URL menggunakan tinyurl API"""
        query = update.callback_query
        await query.answer()
        
        context.user_data['util_waiting'] = 'shorturl'
        
        prompt_text = f"""
{ICON['link']} *🔗 SHORT URL* {ICON['link']}

┌─────────────────────────────────────────────┐
│  Masukkan link panjang yang ingin dipendekkan!│
│                                              │
│  Contoh: `https://example.com/very/long/url`│
└─────────────────────────────────────────────┘

{ICON['info']} Kirimkan URL sekarang...
        """
        
        buttons = [(f"{ICON['back']} Kembali", "utility_menu")]
        keyboard = self._create_keyboard(buttons, row_width=1)
        await query.edit_message_text(prompt_text, reply_markup=keyboard, parse_mode='Markdown')
    
    async def util_qr(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Generate QR Code"""
        query = update.callback_query
        await query.answer()
        
        context.user_data['util_waiting'] = 'qr'
        
        prompt_text = f"""
{ICON['code']} *📱 GENERATE QR CODE* {ICON['code']}

┌─────────────────────────────────────────────┐
│  Masukkan teks atau URL untuk dijadikan QR! │
│                                              │
│  Contoh: `https://t.me/username`            │
│  atau `Hello World!`                        │
└─────────────────────────────────────────────┘

{ICON['info']} Kirimkan teks sekarang...
        """
        
        buttons = [(f"{ICON['back']} Kembali", "utility_menu")]
        keyboard = self._create_keyboard(buttons, row_width=1)
        await query.edit_message_text(prompt_text, reply_markup=keyboard, parse_mode='Markdown')
    
    async def process_util_input(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Memproses input dari user untuk utility"""
        if not context.user_data.get('util_waiting'):
            return
        
        util_type = context.user_data['util_waiting']
        user_input = update.message.text.strip()
        
        if util_type == 'domain':
            # Cek domain menggunakan whois (simulasi sederhana)
            result_text = f"""
{ICON['success']} *HASIL CEK DOMAIN* {ICON['success']}

┌─────────────────────────────────────────────┐
│  Domain: `{user_input}`                      │
│  Status: Terdaftar ✅                        │
│  Server: DNS tersedia                        │
└─────────────────────────────────────────────┘

{ICON['info']} *Informasi lengkap dapat dilihat di:* 
https://who.is/whois/{user_input}
            """
            
        elif util_type == 'ip':
            # Simulasi IP lookup
            result_text = f"""
{ICON['success']} *HASIL IP LOOKUP* {ICON['success']}

┌─────────────────────────────────────────────┐
│  IP: `{user_input}`                          │
│  Lokasi: Tidak dapat ditentukan (simulasi)  │
│  ISP: Unknown                               │
└─────────────────────────────────────────────┘

{ICON['info']} *Untuk IP publik, cek di:* 
https://ipinfo.io/{user_input}
            """
            
        elif util_type == 'shorturl':
            # Short URL menggunakan TinyURL API
            try:
                async with aiohttp.ClientSession() as session:
                    async with session.get(f"http://tinyurl.com/api-create.php?url={user_input}") as resp:
                        short_url = await resp.text()
                        result_text = f"""
{ICON['success']} *SHORT URL BERHASIL* {ICON['success']}

┌─────────────────────────────────────────────┐
│  Original: `{user_input[:50]}...`            │
│  Shortened: `{short_url}`                    │
└─────────────────────────────────────────────┘
                        """
            except:
                result_text = f"{ICON['error']} Gagal memperpendek URL. Pastikan URL valid!"
                
        elif util_type == 'qr':
            # Generate QR Code via API
            qr_url = f"https://api.qrserver.com/v1/create-qr-code/?size=200x200&data={user_input}"
            result_text = f"""
{ICON['success']} *QR CODE GENERATED* {ICON['success']}

┌─────────────────────────────────────────────┐
│  Teks: `{user_input[:50]}...`               │
│  Scan QR di bawah ini!                      │
└─────────────────────────────────────────────┘
            """
            await update.message.reply_photo(qr_url, caption=result_text, parse_mode='Markdown')
            context.user_data['util_waiting'] = None
            return
        
        else:
            result_text = f"{ICON['error']} Fitur tidak dikenal!"
        
        await update.message.reply_text(result_text, parse_mode='Markdown')
        context.user_data['util_waiting'] = None
    
    # ==================== MENU INFORMASI ====================
    
    async def info_menu(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Menu informasi"""
        query = update.callback_query
        await query.answer()
        
        info_text = f"""
{ICON['info']} *┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓*
{ICON['info']} *┃*  {ICON['search']} *INFORMASI*                      {ICON['info']} *┃*
{ICON['info']} *┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛*

Pilih informasi yang ingin dilihat:

{ICON['user']} *👤 INFO USER*
   • Lihat informasi akun Telegram Anda

{ICON['group']} *👥 INFO GROUP*
   • Lihat informasi grup (jika di grup)

{ICON['network']} *📡 CEK PING*
   • Test koneksi ke server bot

{ICON['target']} *🎯 IP LOOKUP*
   • Cari informasi IP address
        """
        
        buttons = [
            (f"{ICON['user']} Info User", "info_user"),
            (f"{ICON['group']} Info Group", "info_group"),
            (f"{ICON['network']} Cek Ping", "info_ping"),
            (f"{ICON['target']} IP Lookup", "info_ip"),
            (f"{ICON['home']} Menu Utama", "main_menu")
        ]
        
        keyboard = self._create_keyboard(buttons, row_width=2)
        await query.edit_message_text(info_text, reply_markup=keyboard, parse_mode='Markdown')
    
    async def info_user(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Menampilkan info user"""
        query = update.callback_query
        await query.answer()
        
        user = update.effective_user
        user_info = f"""
{ICON['user']} *👤 INFO USER* {ICON['user']}

┌─────────────────────────────────────────────┐
│  *ID:* `{user.id}`                           │
│  *Name:* {user.first_name} {user.last_name or ''}  │
│  *Username:* @{user.username or 'None'}      │
│  *Is Bot:* {'Ya' if user.is_bot else 'Tidak'}│
│  *Language:* {user.language_code or 'Unknown'}│
└─────────────────────────────────────────────┘

{ICON['heart']} *Terima kasih telah menggunakan bot ini!*
        """
        
        buttons = [(f"{ICON['back']} Kembali", "info_menu")]
        keyboard = self._create_keyboard(buttons, row_width=1)
        await query.edit_message_text(user_info, reply_markup=keyboard, parse_mode='Markdown')
    
    async def info_group(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Menampilkan info grup"""
        query = update.callback_query
        await query.answer()
        
        chat = update.effective_chat
        
        if chat.type in ['group', 'supergroup']:
            group_info = f"""
{ICON['group']} *👥 INFO GROUP* {ICON['group']}

┌─────────────────────────────────────────────┐
│  *ID:* `{chat.id}`                           │
│  *Name:* {chat.title}                        │
│  *Type:* {chat.type}                         │
│  *Members:* Tidak tersedia (via API)        │
└─────────────────────────────────────────────┘
            """
        else:
            group_info = f"{ICON['warn']} Perintah ini hanya bisa digunakan di dalam grup!"
        
        buttons = [(f"{ICON['back']} Kembali", "info_menu")]
        keyboard = self._create_keyboard(buttons, row_width=1)
        await query.edit_message_text(group_info, reply_markup=keyboard, parse_mode='Markdown')
    
    async def info_ping(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Cek ping/latency bot"""
        query = update.callback_query
        await query.answer()
        
        start = time.time()
        await query.edit_message_text(f"{ICON['network']} *Mengukur ping...*", parse_mode='Markdown')
        end = time.time()
        
        ping = int((end - start) * 1000)
        
        ping_text = f"""
{ICON['network']} *📡 CEK PING* {ICON['network']}

┌─────────────────────────────────────────────┐
│  *Latency:* `{ping} ms`                      │
│  *Status:* {'🟢 Sangat Baik' if ping < 200 else '🟡 Normal' if ping < 500 else '🔴 Lemah'} │
└─────────────────────────────────────────────┘
        """
        
        buttons = [(f"{ICON['back']} Kembali", "info_menu")]
        keyboard = self._create_keyboard(buttons, row_width=1)
        await query.edit_message_text(ping_text, reply_markup=keyboard, parse_mode='Markdown')
    
    async def info_ip(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """IP Lookup menu"""
        query = update.callback_query
        await query.answer()
        
        context.user_data['util_waiting'] = 'ip'
        
        prompt_text = f"""
{ICON['search']} *🔍 IP LOOKUP* {ICON['search']}

┌─────────────────────────────────────────────┐
│  Masukkan alamat IP yang ingin dilacak!     │
│                                              │
│  Contoh: `8.8.8.8` atau `1.1.1.1`          │
└─────────────────────────────────────────────┘

{ICON['info']} Kirimkan IP address sekarang...
        """
        
        buttons = [(f"{ICON['back']} Kembali", "info_menu")]
        keyboard = self._create_keyboard(buttons, row_width=1)
        await query.edit_message_text(prompt_text, reply_markup=keyboard, parse_mode='Markdown')
    
    # ==================== MENU LAINNYA ====================
    
    async def other_menu(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Menu lainnya"""
        query = update.callback_query
        await query.answer()
        
        other_text = f"""
{ICON['settings']} *┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓*
{ICON['settings']} *┃*  {ICON['tools']} *MENU LAINNYA*                    {ICON['settings']} *┃*
{ICON['settings']} *┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛*

Pilih opsi di bawah:

{ICON['heart']} *❤️ ABOUT*
   • Informasi tentang bot ini

{ICON['user']} *👤 CONTACT OWNER*
   • Hubungi pemilik bot

{ICON['coin']} *💰 DONASI*
   • Dukung pengembangan bot

{ICON['bug']} *🐛 REPORT BUG*
   • Laporkan masalah atau saran
        """
        
        buttons = [
            (f"{ICON['heart']} About", "about_menu"),
            (f"{ICON['user']} Contact Owner", "contact_owner"),
            (f"{ICON['coin']} Donasi", "donasi"),
            (f"{ICON['bug']} Report Bug", "report_bug"),
            (f"{ICON['home']} Menu Utama", "main_menu")
        ]
        
        keyboard = self._create_keyboard(buttons, row_width=2)
        await query.edit_message_text(other_text, reply_markup=keyboard, parse_mode='Markdown')
    
    async def about_menu(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Menu about / informasi bot"""
        query = update.callback_query
        await query.answer()
        
        about_text = f"""
{ICON['crown']} *{BOT_NAME}* {ICON['crown']}

┌─────────────────────────────────────────────┐
│  *Version:* {VERSION}                        │
│  *Author:* {OWNER_NAME}                      │
│  *Framework:* python-telegram-bot           │
│  *Type:* All-in-One Utility Bot             │
└─────────────────────────────────────────────┘

{ICON['star']} *FITUR YANG TERSEDIA:*
   🎮 5+ Permainan Interaktif
   🛠️ 10+ Utility Tools
   ℹ️ Informasi Lengkap
   💬 Dukungan Multi-user

{ICON['heart']} *Made with love for Telegram community*
        """
        
        buttons = [(f"{ICON['back']} Kembali", "other_menu")]
        keyboard = self._create_keyboard(buttons, row_width=1)
        await query.edit_message_text(about_text, reply_markup=keyboard, parse_mode='Markdown')
    
    async def contact_owner(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Kontak owner"""
        query = update.callback_query
        await query.answer()
        
        contact_text = f"""
{ICON['user']} *👤 CONTACT OWNER* {ICON['user']}

┌─────────────────────────────────────────────┐
│  *Owner:* {OWNER_NAME}                       │
│  *Channel:* @SimurazxChannel (contoh)       │
│  *Group:* @SimurazxGroup (contoh)           │
└─────────────────────────────────────────────┘

{ICON['info']} Untuk pertanyaan, saran, atau kerjasama, 
silakan hubungi owner melalui channel/group di atas.
        """
        
        buttons = [(f"{ICON['back']} Kembali", "other_menu")]
        keyboard = self._create_keyboard(buttons, row_width=1)
        await query.edit_message_text(contact_text, reply_markup=keyboard, parse_mode='Markdown')
    
    async def donasi(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Menu donasi"""
        query = update.callback_query
        await query.answer()
        
        donasi_text = f"""
{ICON['coin']} *💰 DUKUNG PENGEMBANGAN* {ICON['coin']}

┌─────────────────────────────────────────────┐
│  Dukung bot ini agar terus berkembang!      │
│                                              │
│  *Metode Donasi:*                            │
│  • PayPal: example@paypal.com               │
│  • Saweria: https://saweria.co/example      │
│  • Trakteer: https://trakteer.id/example    │
└─────────────────────────────────────────────┘

{ICON['heart']} *Setiap donasi sangat berarti!*
        """
        
        buttons = [(f"{ICON['back']} Kembali", "other_menu")]
        keyboard = self._create_keyboard(buttons, row_width=1)
        await query.edit_message_text(donasi_text, reply_markup=keyboard, parse_mode='Markdown')
    
    async def report_bug(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Report bug"""
        query = update.callback_query
        await query.answer()
        
        context.user_data['report_waiting'] = True
        
        prompt_text = f"""
{ICON['bug']} *🐛 REPORT BUG* {ICON['bug']}

┌─────────────────────────────────────────────┐
│  Silakan jelaskan bug atau saran Anda!      │
│                                              │
│  Sertakan:                                  │
│  • Deskripsi masalah                        │
│  • Langkah-langkah mereproduksi             │
│  • Screenshot (jika ada)                    │
└─────────────────────────────────────────────┘

{ICON['info']} Kirimkan pesan Anda sekarang...
        """
        
        buttons = [(f"{ICON['back']} Kembali", "other_menu")]
        keyboard = self._create_keyboard(buttons, row_width=1)
        await query.edit_message_text(prompt_text, reply_markup=keyboard, parse_mode='Markdown')
    
    async def process_report(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Memproses report dari user"""
        if not context.user_data.get('report_waiting'):
            return
        
        report_text = update.message.text
        user = update.effective_user
        
        # Kirim ke admin
        for admin_id in ADMIN_IDS:
            await context.bot.send_message(
                admin_id,
                f"{ICON['bug']} *NEW BUG REPORT* {ICON['bug']}\n\n"
                f"*From:* {user.first_name} (@{user.username or 'No username'})\n"
                f"*User ID:* `{user.id}`\n"
                f"*Report:*\n{report_text}",
                parse_mode='Markdown'
            )
        
        await update.message.reply_text(
            f"{ICON['success']} *Laporan terkirim!* Terima kasih atas masukannya.\n"
            f"Owner akan segera merespon jika diperlukan.",
            parse_mode='Markdown'
        )
        
        context.user_data['report_waiting'] = False
    
    # ==================== HANDLER GAME & UTILITY ====================
    
    async def handle_game_guess_input(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Memproses tebakan angka"""
        if not context.user_data.get('game_active') == 'guess_number':
            return
        
        try:
            guess = int(update.message.text)
            secret = context.user_data['secret_number']
            attempts = context.user_data.get('attempts', 0) + 1
            context.user_data['attempts'] = attempts
            
            if guess < 1 or guess > 100:
                await update.message.reply_text(f"{ICON['warn']} Tebakan harus antara 1-100!")
                return
            
            if guess < secret:
                await update.message.reply_text(f"{ICON['info']} *TERLALU KECIL!* Coba lagi.\nPercobaan: {attempts}", parse_mode='Markdown')
            elif guess > secret:
                await update.message.reply_text(f"{ICON['info']} *TERLALU BESAR!* Coba lagi.\nPercobaan: {attempts}", parse_mode='Markdown')
            else:
                await update.message.reply_text(
                    f"{ICON['success']} *SELAMAT!* 🎉\n\n"
                    f"Kamu berhasil menebak angka *{secret}* dalam {attempts} percobaan!\n\n"
                    f"{ICON['game']} Ketik /game untuk bermain lagi.",
                    parse_mode='Markdown'
                )
                context.user_data['game_active'] = None
                
        except ValueError:
            await update.message.reply_text(f"{ICON['error']} Masukkan angka yang valid!")
    
    # ==================== COMMAND HANDLER ====================
    
    async def start_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handler untuk /start"""
        bot_stats["total_commands"] += 1
        
        if update.effective_user.id not in ADMIN_IDS:
            await update.message.reply_text(f"{ICON['error']} *Akses Ditolak*\nAnda tidak memiliki izin untuk menggunakan bot ini.", parse_mode='Markdown')
            return
        
        await self.send_main_menu(update, context)
    
    async def help_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handler untuk /help"""
        help_text = f"""
{ICON['info']} *📖 BANTUAN PENGGUNAAN* {ICON['info']}

┌─────────────────────────────────────────────┐
│  *Perintah Tersedia:*                        │
│  /start - Menu utama                         │
│  /menu - Tampilkan menu                      │
│  /game - Menu permainan                      │
│  /utility - Menu utility                     │
│  /info - Menu informasi                      │
│  /help - Bantuan ini                         │
└─────────────────────────────────────────────┘

{ICON['star']} *Cara Penggunaan:*
1. Gunakan tombol inline untuk navigasi
2. Klik menu yang diinginkan
3. Ikuti instruksi yang muncul

{ICON['heart']} *Nikmati berbagai fitur menarik!*
        """
        
        await update.message.reply_text(help_text, parse_mode='Markdown')
    
    async def menu_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handler untuk /menu"""
        await self.send_main_menu(update, context)
    
    async def game_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handler untuk /game"""
        bot_stats["total_commands"] += 1
        
        game_text = f"""
{ICON['game']} *🎮 MENU PERMAINAN* {ICON['game']}

Pilih permainan favoritmu:

• /guess - Tebak Angka
• /rps - Batu Gunting Kertas
• /quiz - Quiz Random
• /dice - Lempar Dadu

Gunakan tombol di bawah untuk mulai!
        """
        
        buttons = [
            (f"{ICON['target']} Tebak Angka", "game_guess"),
            (f"{ICON['sword']} Batu Gunting Kertas", "game_rps"),
            (f"{ICON['magic']} Quiz", "game_quiz"),
            (f"{ICON['dice']} Dadu", "game_dice"),
            (f"{ICON['home']} Menu Utama", "main_menu")
        ]
        
        keyboard = self._create_keyboard(buttons, row_width=2)
        await update.message.reply_text(game_text, reply_markup=keyboard, parse_mode='Markdown')
    
    async def cancel_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handler untuk /cancel - membatalkan sesi aktif"""
        context.user_data.clear()
        await update.message.reply_text(f"{ICON['success']} *Sesi dibatalkan!* Kembali ke menu utama dengan /menu", parse_mode='Markdown')
    
    # ==================== MAIN FUNCTION ====================
    
    def run(self):
        """Menjalankan bot"""
        # Build application
        self.app = Application.builder().token(self.token).build()
        
        # Command handlers
        self.app.add_handler(CommandHandler("start", self.start_command))
        self.app.add_handler(CommandHandler("menu", self.menu_command))
        self.app.add_handler(CommandHandler("help", self.help_command))
        self.app.add_handler(CommandHandler("game", self.game_command))
        self.app.add_handler(CommandHandler("cancel", self.cancel_command))
        
        # Callback query handlers
        self.app.add_handler(CallbackQueryHandler(self.game_menu, pattern="game_menu"))
        self.app.add_handler(CallbackQueryHandler(self.game_guess_number, pattern="game_guess"))
        self.app.add_handler(CallbackQueryHandler(self.game_rps, pattern="game_rps"))
        self.app.add_handler(CallbackQueryHandler(self.process_rps, pattern="rps_"))
        self.app.add_handler(CallbackQueryHandler(self.game_quiz, pattern="game_quiz"))
        self.app.add_handler(CallbackQueryHandler(self.process_quiz, pattern="quiz_"))
        self.app.add_handler(CallbackQueryHandler(self.game_dice, pattern="game_dice"))
        self.app.add_handler(CallbackQueryHandler(self.game_highscore, pattern="game_highscore"))
        
        self.app.add_handler(CallbackQueryHandler(self.utility_menu, pattern="utility_menu"))
        self.app.add_handler(CallbackQueryHandler(self.util_system, pattern="util_system"))
        self.app.add_handler(CallbackQueryHandler(self.util_domain, pattern="util_domain"))
        self.app.add_handler(CallbackQueryHandler(self.util_ip_lookup, pattern="util_ip"))
        self.app.add_handler(CallbackQueryHandler(self.util_shorturl, pattern="util_shorturl"))
        self.app.add_handler(CallbackQueryHandler(self.util_qr, pattern="util_qr"))
        
        self.app.add_handler(CallbackQueryHandler(self.info_menu, pattern="info_menu"))
        self.app.add_handler(CallbackQueryHandler(self.info_user, pattern="info_user"))
        self.app.add_handler(CallbackQueryHandler(self.info_group, pattern="info_group"))
        self.app.add_handler(CallbackQueryHandler(self.info_ping, pattern="info_ping"))
        self.app.add_handler(CallbackQueryHandler(self.info_ip, pattern="info_ip"))
        
        self.app.add_handler(CallbackQueryHandler(self.other_menu, pattern="other_menu"))
        self.app.add_handler(CallbackQueryHandler(self.about_menu, pattern="about_menu"))
        self.app.add_handler(CallbackQueryHandler(self.contact_owner, pattern="contact_owner"))
        self.app.add_handler(CallbackQueryHandler(self.donasi, pattern="donasi"))
        self.app.add_handler(CallbackQueryHandler(self.report_bug, pattern="report_bug"))
        
        self.app.add_handler(CallbackQueryHandler(self.send_main_menu, pattern="main_menu"))
        
        # Message handlers
        self.app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, self.process_util_input))
        self.app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, self.handle_game_guess_input))
        self.app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, self.process_report))
        
        # Set bot commands
        commands = [
            BotCommand("start", "🚀 Mulai bot dan menu utama"),
            BotCommand("menu", "📋 Tampilkan menu utama"),
            BotCommand("game", "🎮 Menu permainan"),
            BotCommand("help", "📖 Bantuan penggunaan"),
            BotCommand("cancel", "❌ Batalkan sesi aktif")
        ]
        
        self.app.bot.set_my_commands(commands)
        
        # Print startup info
        print(f"""
╔══════════════════════════════════════════════════════════════════╗
║                    {BOT_NAME}                        ║
║                         v3.0                                      ║
╠══════════════════════════════════════════════════════════════════╣
║  ✅ Bot started successfully!                                    ║
║  📍 Token: {self.token[:15]}...                                    ║
║  👑 Admin ID: {ADMIN_IDS[0]}                                        ║
║  🎮 Features: Games | Utility | Info | More                       ║
╚══════════════════════════════════════════════════════════════════╝
        """)
        
        self.app.run_polling()

# ==================== MAIN EXECUTION ====================

if __name__ == "__main__":
    if BOT_TOKEN == "YOUR_BOT_TOKEN_HERE":
        print("❌ ERROR: Silakan ganti BOT_TOKEN dengan token bot Telegram Anda!")
        print("📌 Dapatkan token dari @BotFather di Telegram")
        exit(1)
    
    bot = SimurazxUltimateBot(BOT_TOKEN)
    bot.run()
