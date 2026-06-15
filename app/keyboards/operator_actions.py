from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from app.callbacks.operator_actions import OperatorActionCallback


def operator_request_keyboard(client_id: int) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(
        text="Взяти в роботу",
        callback_data=OperatorActionCallback(
            action="take",
            client_id=client_id,
        ).pack(),
    )
    builder.button(
        text="Закрити",
        callback_data=OperatorActionCallback(
            action="close",
            client_id=client_id,
        ).pack(),
    )
    builder.adjust(1)
    return builder.as_markup()


def operator_active_keyboard(client_id: int) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(
        text="Закрити звернення",
        callback_data=OperatorActionCallback(
            action="close",
            client_id=client_id,
        ).pack(),
    )
    builder.button(
        text="Повернути боту",
        callback_data=OperatorActionCallback(
            action="bot",
            client_id=client_id,
        ).pack(),
    )
    builder.adjust(1)
    return builder.as_markup()