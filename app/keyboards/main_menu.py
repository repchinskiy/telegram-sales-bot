from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder


def main_menu_keyboard() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(text="Тарифи та ціни", callback_data="menu:tariffs")
    builder.button(text="Підключення", callback_data="menu:connection")
    builder.button(text="Потрібна консультація", callback_data="menu:consultation")
    builder.button(text="Покликати оператора", callback_data="menu:operator")
    builder.adjust(1)
    return builder.as_markup()