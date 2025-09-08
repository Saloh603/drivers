from aiogram.fsm.state import State, StatesGroup

class PassengerStates(StatesGroup):
    waiting_for_number = State()
    waiting_for_destination = State()
    waiting_for_time = State()
    waiting_for_people_count = State()
