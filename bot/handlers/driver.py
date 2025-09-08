from aiogram import Router, types, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from bot.states.driver_states import DriverStates

router = Router()

@router.message(Command("driver"))
async def start_driver(message: types.Message, state: FSMContext):
    await message.answer("Please send me your phone number 📱")
    await state.set_state(DriverStates.waiting_for_number)

@router.message(DriverStates.waiting_for_number, F.text)
async def driver_number(message: types.Message, state: FSMContext):
    await state.update_data(phone=message.text)
    await message.answer("When will you depart? (e.g. 18:00 today)")
    await state.set_state(DriverStates.waiting_for_departure_time)

@router.message(DriverStates.waiting_for_departure_time, F.text)
async def driver_time(message: types.Message, state: FSMContext):
    await state.update_data(time=message.text)
    await message.answer("From where will you depart? 🚏")
    await state.set_state(DriverStates.waiting_for_departure_place)

@router.message(DriverStates.waiting_for_departure_place, F.text)
async def driver_place(message: types.Message, state: FSMContext):
    await state.update_data(place=message.text)
    data = await state.get_data()
    await message.answer(
        f"✅ Driver registered!\n\n"
        f"📱 Phone: {data['phone']}\n"
        f"⏰ Time: {data['time']}\n"
        f"🚏 Place: {data['place']}"
    )
    await state.clear()
