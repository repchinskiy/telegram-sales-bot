from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message

from app.keyboards.main_menu import main_menu_keyboard
from app.services.container import ServiceContainer

router = Router()


@router.message(CommandStart())
async def cmd_start(message: Message, container: ServiceContainer) -> None:
    conversation = container.conversations.get_or_create(message.from_user.id)
    conversation.mode = "bot"
    conversation.stage = "welcome"
    await message.answer(
        container.dialogs.welcome_text(),
        reply_markup=main_menu_keyboard(),
    )