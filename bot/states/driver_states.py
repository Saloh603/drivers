from aiogram.fsm.state import StatesGroup, State

class DriverStates(StatesGroup):
    waiting_for_number = State()
    waiting_for_destination = State()
    waiting_for_trip_type = State()   # Daily or Specific date
    waiting_for_date = State()
    waiting_for_time = State()
    waiting_for_seats = State()
