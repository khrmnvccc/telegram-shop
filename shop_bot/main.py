import asyncio

from aiogram import Bot, Dispatcher
from aiogram.filters import Command
from aiogram.types import Message, KeyboardButton, ReplyKeyboardMarkup
from aiogram.fsm.context import FSMContext

from shop_bot.states import AddProduct
from shop_bot.keyboards import menu
from shop_bot.config import TOKEN, ADMIN_ID

bot = Bot(token=TOKEN)
dp = Dispatcher()

phone_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(
                text="📱 Telefon raqamni yuborish",
                request_contact=True
            )
        ]
    ],
    resize_keyboard=True
)

@dp.message(Command("start"))
async def start(message: Message):

    await message.answer(
        "Assalomu alaykum!\n\n"
        "Davom etish uchun telefon raqamingizni yuboring.",
        reply_markup=phone_keyboard
    )

@dp.message(lambda message: message.contact)
async def save_phone(message: Message):

    phone = message.contact.phone_number
    chat_id = str(message.chat.id)

    db = sqlite3.connect("database.db")
    cursor = db.cursor()

    cursor.execute("""
        INSERT OR REPLACE INTO telegram_users(phone, chat_id)
        VALUES (?, ?)
    """, (phone, chat_id))

    db.commit()
    db.close()

    await message.answer(
        "✅ Telefon raqamingiz saqlandi.\n"
        "Endi saytda ro'yxatdan o'tishingiz mumkin."
    )

@dp.message(Command("add"))
async def add_product(message: Message, state: FSMContext):
    from config import ADMIN_ID

    if message.from_user.id != ADMIN_ID:
        await message.answer("❌ Bu buyruq faqat admin uchun.")
        return

    await state.set_state(AddProduct.photo)
    await message.answer("📷 Mahsulot rasmini yuboring.")
@dp.message(AddProduct.photo)
async def get_photo(message: Message, state: FSMContext):
    if not message.photo:
        await message.answer("❌ Rasm yuboring.")
        return

    await state.update_data(photo=message.photo[-1].file_id)
    await state.set_state(AddProduct.name)
    await message.answer("📝 Mahsulot nomini yozing.")
   
@dp.message()
async def messages(message: Message):
    if message.text == "🛍 Mahsulotlar":
        await message.answer("🛍 Hozircha mahsulotlar qo'shilmagan.")
        return

    if message.text == "🛒 Buyurtma":
        await message.answer("📝 Buyurtma bo'limi hali tayyorlanmoqda.")
        return

    if message.text == "📞 Aloqa":
        await message.answer(
            "📞 Aloqa uchun:\n"
            "@asia_box_cn\n"
            "+998 98 577 12 26  "
        )
        return

    await message.answer("Iltimos, pastdagi tugmalardan foydalaning.")


async def main():
    print("✅ Bot ishga tushdi")
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
