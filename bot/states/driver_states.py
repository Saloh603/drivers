from aiogram.fsm.state import State, StatesGroup

class DriverStates(StatesGroup):
    waiting_for_number = State()
    waiting_for_departure_time = State()
    waiting_for_departure_place = State()
