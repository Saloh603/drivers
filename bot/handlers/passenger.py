from aiogram import Router, types, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from bot.states.passenger_states import PassengerStates

router = Router()

@router.message(Command("passenger"))
async def start_passenger(message: types.Message, state: FSMContext):
    await message.answer("Please send me your phone number 📱")
    await state.set_state(PassengerStates.waiting_for_number)

@router.message(PassengerStates.waiting_for_number, F.text)
async def passenger_number(message: types.Message, state: FSMContext):
    await state.update_data(phone=message.text)
    await message.answer("Where do you want to go? 🏙")
    await state.set_state(PassengerStates.waiting_for_destination)

@router.message(PassengerStates.waiting_for_destination, F.text)
async def passenger_destination(message: types.Message, state: FSMContext):
    await state.update_data(destination=message.text)
    await message.answer("When do you want to go? (e.g. 19:00 today)")
    await state.set_state(PassengerStates.waiting_for_time)

@router.message(PassengerStates.waiting_for_time, F.text)
async def passenger_time(message: types.Message, state: FSMContext):
    await state.update_data(time=message.text)
    await message.answer("How many people? 👥")
    await state.set_state(PassengerStates.waiting_for_people_count)

@router.message(PassengerStates.waiting_for_people_count, F.text)
async def passenger_people(message: types.Message, state: FSMContext):
    await state.update_data(people=message.text)
    data = await state.get_data()
    await message.answer(
        f"✅ Passenger registered!\n\n"
        f"📱 Phone: {data['phone']}\n"
        f"🏙 Destination: {data['destination']}\n"
        f"⏰ Time: {data['time']}\n"
        f"👥 People: {data['people']}"
    )
    await state.clear()
