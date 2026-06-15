from aiogram import Dispatcher

from app.handlers.menu import router as menu_router
from app.handlers.messages import router as message_router
from app.handlers.operator import router as operator_router
from app.handlers.start import router as start_router


def register_handlers(dp: Dispatcher) -> None:
    dp.include_router(start_router)
    dp.include_router(menu_router)
    dp.include_router(operator_router)
    dp.include_router(message_router)