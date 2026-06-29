import asyncio

from aiogram import Bot, Dispatcher
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from states import AddProduct

from config import TOKEN
from keyboards import menu

bot = Bot(token=TOKEN)
dp = Dispatcher()

@dp.message(Command("start"))
async def start(message: Message):
    await message.answer(
        "🇺🇿 Assalomu alaykum!\n\n"
"🛍 Asia Box botiga xush kelibsiz!\n\n"
"Pastdagi menyudan kerakli bo'limni tanlang.",
        reply_markup=menu
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
