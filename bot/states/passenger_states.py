from aiogram.fsm.state import StatesGroup, State

class PassengerStates(StatesGroup):
    waiting_for_number = State()
    waiting_for_destination = State()
    waiting_for_date = State()
    waiting_for_time = State()
    waiting_for_seats = State()
