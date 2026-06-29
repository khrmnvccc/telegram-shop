from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

menu = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="🛍 Mahsulotlar")],
        [KeyboardButton(text="🛒 Buyurtma")],
        [KeyboardButton(text="📞 Aloqa")]
    ],
    resize_keyboard=True
)