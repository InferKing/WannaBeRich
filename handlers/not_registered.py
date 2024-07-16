from aiogram import Router, F
from aiogram.types import Message
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from db import create_user
from filters import UnregisterUserFilter
from localization import get_message
from aiogram.utils.formatting import Bold, as_marked_list, as_marked_section, Underline, as_line

router = Router()


class StartStates(StatesGroup):
    balance = State()


@router.message(StartStates.balance, F.text.regexp(r"^[+-]?[1-9]\d*$|^0$"))
async def cmd_start_balance(message: Message, state: FSMContext):
    balance = int(message.text)
    lang = message.from_user.language_code
    await state.clear()
    await message.answer(get_message("new_user_success", lang))
    await create_user(message.from_user.id, message.from_user.username, balance)

@router.message(StartStates.balance)
async def cmd_start_balance_error(message: Message, state: FSMContext):
    lang = message.from_user.language_code
    await message.answer(get_message("new_user_error", lang))


@router.message(F.text, UnregisterUserFilter())
async def cmd_new_user(message: Message, state: FSMContext):
    lang = message.from_user.language_code
    await message.answer(get_message("new_user_title", lang))
    await message.answer(**as_marked_list(
        as_marked_section(
            Bold("‼️ " + get_message("new_user_body", lang) + "\n"),
            "100",
            "-100",
            marker="-> 💰 "
        ),
        "",
        Underline("‼️ " + get_message("value_helper", lang)),
        marker=""
    ).as_kwargs())

    await state.set_state(StartStates.balance)