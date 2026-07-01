import sqlite3
import telebot
from telebot.types import ReplyKeyboardMarkup, KeyboardButton, WebAppInfo

from config import TOKEN

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=["start"])
def start(message):

    db = sqlite3.connect("database.db")
    cursor = db.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS telegram_users(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            chat_id INTEGER UNIQUE,
            phone TEXT
        )
    """)

    cursor.execute(
        "INSERT OR IGNORE INTO telegram_users(chat_id) VALUES (?)",
        (message.chat.id,)
    )

    db.commit()
    db.close()

    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)

    keyboard.add(
    KeyboardButton(
        text="📱 Telefon raqamni yuborish",
        request_contact=True
    )
)

    bot.send_message(
    message.chat.id,
    "👋 Assalomu alaykum!\n\n"
    "🔐 Saytda ro'yxatdan o'tish uchun avval telefon raqamingizni yuboring.\n\n"
    "📲 Pastdagi «Telefon raqamni yuborish» tugmasini bosing.",
    reply_markup=keyboard
)


print("🤖 Bot ishga tushdi...")

@bot.message_handler(content_types=['contact'])
def save_contact(message):

    phone = message.contact.phone_number.replace("+","")
    chat_id = message.chat.id

    db = sqlite3.connect("database.db")
    cursor = db.cursor()

    cursor.execute("""
        UPDATE telegram_users
        SET phone=?
        WHERE chat_id=?
    """, (phone, chat_id))

    db.commit()
    db.close()

    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)

    keyboard.add(
        KeyboardButton(
            text="🛍 Do'kon",
            web_app=WebAppInfo("https://YOUR-DOMAIN.onrender.com")
        )
    )

    bot.send_message(
    chat_id,
    "✅ Telefon raqamingiz muvaffaqiyatli saqlandi!\n\n"
    "1️⃣ Saytga kiring.\n"
    "2️⃣ Shu telefon raqami bilan ro'yxatdan o'ting.\n"
    "3️⃣ @Asia_Store_uz_bot botiga /start bosing.\n"
    "4️⃣ Tasdiqlash kodi shu bot orqali yuboriladi.",
    reply_markup=keyboard
)

bot.infinity_polling(skip_pending=True)