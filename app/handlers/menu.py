from aiogram import F, Router
from aiogram.types import CallbackQuery

from app.keyboards.main_menu import main_menu_keyboard
from app.services.container import ServiceContainer

router = Router()


@router.callback_query(F.data.startswith("menu:"))
async def process_menu(
    callback: CallbackQuery,
    container: ServiceContainer,
) -> None:
    action = callback.data.split(":", 1)[1]
    user_id = callback.from_user.id

    if action == "tariffs":
        container.conversations.update_stage(user_id, "tariffs")
        await callback.message.answer(container.dialogs.tariffs_text())

    elif action == "connection":
        container.conversations.update_stage(user_id, "connection")
        await callback.message.answer(container.dialogs.connection_text())

    elif action == "consultation":
        container.conversations.update_stage(user_id, "consultation")
        await callback.message.answer(container.dialogs.consultation_text())

    elif action == "operator":
        await container.handoff.request_operator_from_callback(
            callback,
            reason="manual_button",
        )
        return

    elif action == "back":
        await callback.message.answer(
            container.dialogs.welcome_text(),
            reply_markup=main_menu_keyboard(),
        )

    await callback.answer()