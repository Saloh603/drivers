from aiogram import Router, types
from aiogram.filters import Command

router = Router()

@router.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer(f"""Assalomu alekum haydovchimisiz yoki yo'ovchi.\n
    Agar haydovchi bo'lsangiz /driver
    Agar yo'lovchi bo'lsangiz /passanger tugmasini bosing.""")
