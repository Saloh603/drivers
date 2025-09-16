from aiogram import Router, types, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove, CallbackQuery
from aiogram_calendar import SimpleCalendar, SimpleCalendarCallback
from bot.states.driver_states import DriverStates

router = Router()

@router.message(Command("driver"))
async def start_driver(message: types.Message, state: FSMContext):
    user_name = message.from_user.first_name

    kb = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="📱 Share my number", request_contact=True)]
        ],
        resize_keyboard=True,
        one_time_keyboard=True
    )

    await message.answer(
        f"Hello {user_name}, this is the Driver registration 🚖\n\n"
        "Please share your phone number to continue.",
        reply_markup=kb
    )
    await state.set_state(DriverStates.waiting_for_number)


@router.message(DriverStates.waiting_for_number, F.contact)
async def driver_number(message: types.Message, state: FSMContext):
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

    await message.answer("Where are you driving to?", reply_markup=kb)
    await state.set_state(DriverStates.waiting_for_destination)


@router.message(DriverStates.waiting_for_destination, F.text.in_(["Tashkent", "Zarafshan"]))
async def driver_destination(message: types.Message, state: FSMContext):
    await state.update_data(destination=message.text)

    kb = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="🚘 Daily trip")],
            [KeyboardButton(text="📅 Specific date")]
        ],
        resize_keyboard=True,
        one_time_keyboard=True
    )

    await message.answer(
        "Do you drive daily or only on a specific date?",
        reply_markup=kb
    )
    await state.set_state(DriverStates.waiting_for_trip_type)


@router.message(DriverStates.waiting_for_trip_type, F.text.in_(["🚘 Daily trip", "📅 Specific date"]))
async def driver_trip_type(message: types.Message, state: FSMContext):
    trip_type = message.text
    await state.update_data(trip_type=trip_type)

    if trip_type == "🚘 Daily trip":
        # Go directly to time selection
        kb = ReplyKeyboardMarkup(
            keyboard=[
                [KeyboardButton(text="08:00"), KeyboardButton(text="12:00")],
                [KeyboardButton(text="18:00"), KeyboardButton(text="21:00")]
            ],
            resize_keyboard=True,
            one_time_keyboard=True
        )
        await message.answer("⏰ What time do you usually depart?", reply_markup=kb)
        await state.set_state(DriverStates.waiting_for_time)

    else:
        # Show inline calendar
        await message.answer(
            "📅 Please choose your departure date:",
            reply_markup=await SimpleCalendar().start_calendar()
        )
        await state.set_state(DriverStates.waiting_for_date)


@router.callback_query(SimpleCalendarCallback.filter(), DriverStates.waiting_for_date)
async def driver_date(callback_query: CallbackQuery, callback_data: dict, state: FSMContext):
    selected, date = await SimpleCalendar().process_selection(callback_query, callback_data)
    if selected:
        await state.update_data(date=date.strftime("%Y-%m-%d"))

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
        await state.set_state(DriverStates.waiting_for_time)


@router.message(DriverStates.waiting_for_time, F.text.in_(["08:00", "12:00", "18:00", "21:00"]))
async def driver_time(message: types.Message, state: FSMContext):
    await state.update_data(time=message.text)

    kb = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="1"), KeyboardButton(text="2")],
            [KeyboardButton(text="3"), KeyboardButton(text="4")]
        ],
        resize_keyboard=True,
        one_time_keyboard=True
    )

    await message.answer("How many free seats do you have?", reply_markup=kb)
    await state.set_state(DriverStates.waiting_for_seats)


@router.message(DriverStates.waiting_for_seats, F.text.in_(["1", "2", "3", "4"]))
async def driver_seats(message: types.Message, state: FSMContext):
    await state.update_data(seats=int(message.text))
    data = await state.get_data()

    await message.answer(
        f"✅ Driver profile saved!\n\n"
        f"Destination: {data['destination']}\n"
        f"Trip type: {data['trip_type']}\n"
        f"Date: {data.get('date', 'Every day')}\n"
        f"Time: {data['time']}\n"
        f"Seats: {data['seats']}\n\n"
        "Passengers will now see your trip 🚖",
        reply_markup=ReplyKeyboardRemove()
    )
