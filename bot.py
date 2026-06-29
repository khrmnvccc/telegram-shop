import telebot
from telebot.types import ReplyKeyboardMarkup, KeyboardButton, WebAppInfo

from config import TOKEN

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def start(message):
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)

    keyboard.add(
        KeyboardButton(
            text="🛍 Do'kon",
            web_app=WebAppInfo("https://YOUR-DOMAIN.onrender.com")
        )
    )

    bot.send_message(
        message.chat.id,
        "Assalomu alaykum!\n\nDo'konimizga xush kelibsiz!",
        reply_markup=keyboard
    )
print("🤖 Bot ishga tushdi...")

try:
    bot.infinity_polling(skip_pending=True)
except Exception as e:
    print(e)
