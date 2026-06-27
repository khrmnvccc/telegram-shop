import telebot
from telebot.types import ReplyKeyboardMarkup, KeyboardButton
from config import TOKEN

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def start(message):
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)

    keyboard.add(
        KeyboardButton("🛍 Do'kon")
    )

    bot.send_message(
        message.chat.id,
        "Assalomu alaykum!\n\nDo'konimizga xush kelibsiz!",
        reply_markup=keyboard
    )

@bot.message_handler(func=lambda message: message.text == "🛍 Do'kon")
def shop(message):
    bot.send_message(
        message.chat.id,
        "Mini App tez orada shu tugma orqali ochiladi."
    )

print("Bot ishga tushdi...")
bot.infinity_polling()

print("Bot ishga tushdi")

try:
    bot.infinity_polling()
except Exception as e:
    print(e)
    