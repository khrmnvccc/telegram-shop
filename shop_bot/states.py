from aiogram.fsm.state import StatesGroup, State

class AddProduct(StatesGroup):
    photo = State()
    name = State()
    price = State()