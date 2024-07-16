from aiogram.utils.keyboard import InlineKeyboardBuilder, InlineKeyboardButton
from aiogram.types import KeyboardButton
from localization import get_message

def get_start_keyboard(lang: str) -> InlineKeyboardBuilder:
    kb = InlineKeyboardBuilder()
    kb.add(InlineKeyboardButton(text=get_message("action_add", lang), callback_data="add_economy"))
    kb.add(InlineKeyboardButton(text=get_message("update_category", lang), callback_data="update_category"))
    kb.add(InlineKeyboardButton(text=get_message("remove_category", lang), callback_data="remove_category"))
    kb.add(InlineKeyboardButton(text=get_message("action_show_stat", lang), callback_data="show_stat"))
    kb.adjust(1, 2, 1)
    return kb


def get_cancel_keyboard(lang: str) -> InlineKeyboardBuilder:
    kb = InlineKeyboardBuilder()
    kb.add(InlineKeyboardButton(text=get_message("cancel", lang), callback_data="cancel"))
    kb.adjust(1)
    return kb