from aiogram import Router, F
from aiogram.utils.formatting import Bold, as_marked_list, as_marked_section, Underline, as_line
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command, CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import Message, ReplyKeyboardRemove
from localization import get_message
from keyboards import start
from db import find_user_by_id, create_user, create_category, get_categories, get_expenses, get_incomes, get_economy, create_economy
from filters import RegisterUserFilter, UnregisterUserFilter


router = Router()


class EconomyStates(StatesGroup):
    amount = State()
    category = State()


@router.message(CommandStart(), RegisterUserFilter())
async def cmd_start(message: Message, state: FSMContext):
    await state.clear()
    lang = message.from_user.language_code
    await message.answer(
        **as_line(
            Bold(get_message("start", lang)),
            Bold(get_message("powered_by", lang)),
            sep="\n\n"
        ).as_kwargs()
    )



@router.message(Command("menu"), RegisterUserFilter())
async def cmd_menu(message: Message, state: FSMContext):
    await state.clear()
    lang = message.from_user.language_code
    await message.answer(get_message("menu", lang), reply_markup=start.get_start_keyboard(lang).as_markup(one_time_keyboard=True))

@router.callback_query(F.data == "cancel")
async def cmd_cancel(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    await callback.message.delete()
    await callback.message.answer(get_message("cancel_msg", callback.from_user.language_code))

@router.callback_query(F.data == "add_economy")
async def cmd_add_income(callback: CallbackQuery, state: FSMContext):
    lang = callback.from_user.language_code
    await callback.message.answer(**as_marked_list(
        as_marked_section(
            Bold("‼️ " + get_message("economy_amount", lang) + "\n"),
            "100",
            "-100",
            marker="-> 💰 "
        ),
        "",
        Underline("‼️ " + get_message("value_helper", lang)),
        marker=""
    ).as_kwargs(),
        reply_markup=start.get_cancel_keyboard(lang).as_markup(one_time_keyboard=True))
    await state.set_state(EconomyStates.amount)

@router.message(EconomyStates.amount, F.text.regexp(r"^[+-]?[1-9]\d*$|^0$"))
async def answer_income_amount(message: Message, state: FSMContext):
    await state.update_data(amount=message.text)
    data = await get_categories(message.from_user.id)
    lang = message.from_user.language_code
    if not data:
        await message.answer(get_message("choose_category_empty", lang),
        reply_markup=start.get_cancel_keyboard(lang).as_markup(one_time_keyboard=True))
    else:
        await message.answer(**as_marked_list(
            as_marked_section(
                Bold(get_message("choose_category", lang) + "\n"),
                *list(map(lambda x: x.name.capitalize(), data)),
                marker="-> 🔹 "
            )
        ).as_kwargs(), reply_markup=start.get_cancel_keyboard(lang).as_markup(one_time_keyboard=True))
    await state.set_state(EconomyStates.category)

# хендлер ловит неправильные значения дохода
@router.message(EconomyStates.amount)
async def answer_income_amount(message: Message, state: FSMContext):
    await message.answer(get_message("economy_amount_error", message.from_user.language_code))


@router.message(EconomyStates.category, F.text)
async def answer_income_category(message: Message, state: FSMContext):
    await state.update_data(category=message.text)
    data = await state.get_data()
    user = await find_user_by_id(message.from_user.id)
    categories = await get_categories(message.from_user.id)
    category = data["category"].strip().lower() 
    if category not in list(map(lambda x: x.name.lower(), categories)):
        result_cat = await create_category(message.from_user.id, category)
    else:
        result_cat = await get_categories(message.from_user.id)
        result_cat = list(filter(lambda x: x.name.lower() == category, result_cat))[0]
    amount = int(data["amount"])
    await create_economy(message.from_user.id, result_cat.id, amount)
    await message.answer(get_message("economy_added", message.from_user.language_code, amount=amount, category=category))
    await state.clear()