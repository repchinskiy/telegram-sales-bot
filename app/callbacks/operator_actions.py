from aiogram.filters.callback_data import CallbackData


class OperatorActionCallback(CallbackData, prefix="op"):
    action: str
    client_id: int