from aiogram import Router, types, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove, CallbackQuery
from aiogram_calendar import SimpleCalendar, SimpleCalendarCallback
from bot.states.passenger_states import PassengerStates
from datetime import datetime

router = Router()

@router.message(Command("passenger"))
async def start_passenger(message: types.Message, state: FSMContext):
    user_name = message.from_user.first_name

    kb = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="📱 Share my number", request_contact=True)]
        ],
        resize_keyboard=True,
        one_time_keyboard=True
    )

    await message.answer(
        f"Hello {user_name}, this is a Taxi bot 🚖\n\n"
        "Please share your phone number to continue.",
        reply_markup=kb
    )
    await state.set_state(PassengerStates.waiting_for_number)


@router.message(PassengerStates.waiting_for_number, F.contact)
async def passenger_number(message: types.Message, state: FSMContext):
    phone = message.contact.phone_number
    await state.update_data(phone=phone)

    kb = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="Tashkent")],
            [KeyboardButton(text="Zarafshan")]
        ],
        resize_keyboard=True,
        one_time_keyboard=True
    )

    await message.answer(
        "✅ Thank you! Now, where do you want to go?",
        reply_markup=kb
    )
    await state.set_state(PassengerStates.waiting_for_destination)


@router.message(PassengerStates.waiting_for_destination, F.text.in_(["Tashkent", "Zarafshan"]))
async def passenger_destination(message: types.Message, state: FSMContext):
    await state.update_data(destination=message.text)

    # Show inline calendar
    await message.answer(
        "📅 Please choose your travel date:",
        reply_markup=await SimpleCalendar().start_calendar()
    )
    await state.set_state(PassengerStates.waiting_for_date)


@router.callback_query(SimpleCalendarCallback.filter(), PassengerStates.waiting_for_date)
async def passenger_date(callback_query: CallbackQuery, callback_data: dict, state: FSMContext):
    selected, date = await SimpleCalendar().process_selection(callback_query, callback_data)
    if selected:
        await state.update_data(date=date.strftime("%Y-%m-%d"))

        # Time slot buttons
        kb = ReplyKeyboardMarkup(
            keyboard=[
                [KeyboardButton(text="08:00"), KeyboardButton(text="12:00")],
                [KeyboardButton(text="18:00"), KeyboardButton(text="21:00")]
            ],
            resize_keyboard=True,
            one_time_keyboard=True
        )

        await callback_query.message.answer(
            f"✅ Date chosen: {date.strftime('%Y-%m-%d')}\n\n"
            "⏰ Now select your departure time:",
            reply_markup=kb
        )
        await state.set_state(PassengerStates.waiting_for_time)


@router.message(PassengerStates.waiting_for_time, F.text.in_(["08:00", "12:00", "18:00", "21:00"]))
async def passenger_time(message: types.Message, state: FSMContext):
    await state.update_data(time=message.text)

    # Seats selection
    kb = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="1"), KeyboardButton(text="2")],
            [KeyboardButton(text="3"), KeyboardButton(text="4")]
        ],
        resize_keyboard=True,
        one_time_keyboard=True
    )

    await message.answer(
        "👍 Got it! How many people will travel with you?",
        reply_markup=kb
    )
    await state.set_state(PassengerStates.waiting_for_seats)


@router.message(PassengerStates.waiting_for_seats, F.text.in_(["1", "2", "3", "4"]))
async def passenger_seats(message: types.Message, state: FSMContext):
    await state.update_data(seats=int(message.text))
    data = await state.get_data()

    await message.answer(
        f"✅ Saved!\n\n"
        f"Destination: {data['destination']}\n"
        f"Date: {data['date']}\n"
        f"Time: {data['time']}\n"
        f"Seats: {data['seats']}\n\n"
        "Next step → I will show you available drivers 🚖",
        reply_markup=ReplyKeyboardRemove()
    )
