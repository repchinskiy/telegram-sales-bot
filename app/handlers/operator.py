from aiogram import F, Router
from aiogram.types import CallbackQuery, Message

from app.callbacks.operator_actions import OperatorActionCallback
from app.keyboards.operator_actions import operator_active_keyboard
from app.services.container import ServiceContainer

router = Router()
router.message.filter(F.chat.type.in_({"group", "supergroup"}))


@router.callback_query(OperatorActionCallback.filter())
async def operator_action_handler(
    callback: CallbackQuery,
    callback_data: OperatorActionCallback,
    container: ServiceContainer,
) -> None:
    if callback.message.chat.id != container.handoff.operator_chat_id:
        await callback.answer("Недоступно", show_alert=True)
        return

    client_id = callback_data.client_id
    action = callback_data.action
    operator = callback.from_user

    conversation = container.conversations.get_or_create(client_id)

    if action == "take":
        if conversation.assigned_operator_id and conversation.assigned_operator_id != operator.id:
            await callback.answer("Діалог уже закріплений за іншим оператором.", show_alert=True)
            return

        container.conversations.assign_operator(
            client_id,
            operator.id,
            request_message_id=callback.message.message_id,
        )

        updated_text = (
            f"{callback.message.html_text}\n\n"
            f"<b>Статус:</b> в роботі\n"
            f"<b>Оператор:</b> {operator.full_name} (@{operator.username or '-'})"
        )

        await callback.message.edit_text(
            updated_text,
            reply_markup=operator_active_keyboard(client_id),
        )
        await callback.bot.send_message(
            chat_id=client_id,
            text=(
                "Доброго дня ! "
                "Чим можу допогти ?"
            ),
        )
        await callback.answer("Діалог взято в роботу")
        return

    if action == "close":
        container.conversations.close(client_id)

        updated_text = f"{callback.message.html_text}\n\n<b>Статус:</b> закрито"

        await callback.message.edit_text(updated_text)
        await callback.bot.send_message(
            chat_id=client_id,
            text=(
                "Ваше звернення завершено. "
                "Якщо виникнуть нові питання, просто напишіть у цей чат."
            ),
        )
        await callback.answer("Звернення закрито")
        return

    if action == "bot":
        container.conversations.back_to_bot(client_id)

        updated_text = f"{callback.message.html_text}\n\n<b>Статус:</b> повернуто боту"

        await callback.message.edit_text(updated_text)
        await callback.bot.send_message(
            chat_id=client_id,
            text=(
                "Діалог повернуто до автоматичного режиму. "
                "Ви можете продовжити спілкування з ботом."
            ),
        )
        await callback.answer("Повернуто боту")
        return

    await callback.answer()


@router.message(F.reply_to_message)
async def operator_reply_handler(
    message: Message,
    container: ServiceContainer,
) -> None:
    if message.chat.id != container.handoff.operator_chat_id:
        return

    if not message.text:
        return

    replied_message_id = message.reply_to_message.message_id
    client_id = container.bridge.get_client_id(replied_message_id)

    if not client_id:
        return

    conversation = container.conversations.get(client_id)
    if not conversation:
        await message.reply("Діалог не знайдено.")
        return

    if conversation.mode not in {"human", "handoff_requested"}:
        await message.reply("Діалог не активний для відповіді оператором.")
        return

    if conversation.assigned_operator_id and conversation.assigned_operator_id != message.from_user.id:
        await message.reply("Цей діалог закріплений за іншим оператором.")
        return

    if conversation.mode == "handoff_requested" and not conversation.assigned_operator_id:
        await message.reply("Спочатку натисніть «Взяти в роботу».")
        return

    await container.handoff.send_operator_reply_to_client(message, client_id)
    await message.reply("Відповідь надіслано клієнту.")