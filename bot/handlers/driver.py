from aiogram import Router, types, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from bot.states.driver_states import DriverStates

router = Router()

@router.message(Command("driver"))
async def start_driver(message: types.Message, state: FSMContext):
    # User’s first name
    user_name = message.from_user.first_name

    # Button to share contact
    kb = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="📱 Share my number", request_contact=True)]
        ],
        resize_keyboard=True,
        one_time_keyboard=True
    )

    await message.answer(
        f"Salom {user_name}, bu Taxi bot 🚖\n\n"
        "menga nomeringizni bera olasizmi registratsiya uchun?",
        reply_markup=kb
    )
    await state.set_state(DriverStates.waiting_for_number)


@router.message(DriverStates.waiting_for_number, F.contact)
async def driver_number(message: types.Message, state: FSMContext):
    phone = message.contact.phone_number
    await state.update_data(phone=phone)

    await message.answer(
        "✅ Thanks! Now tell me when you will depart ⏰",
        reply_markup=types.ReplyKeyboardRemove()
    )
    await state.set_state(DriverStates.waiting_for_departure_time)
