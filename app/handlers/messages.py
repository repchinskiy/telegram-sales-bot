import re

from aiogram import Router
from aiogram.types import Message

from app.keyboards.main_menu import main_menu_keyboard
from app.services.container import ServiceContainer

router = Router()

PHONE_REGEX = re.compile(r"\+?\d[\d\s\-\(\)]{7,}\d")


def extract_phone(text: str) -> str | None:
    match = PHONE_REGEX.search(text)
    if not match:
        return None

    phone = match.group(0)
    phone = re.sub(r"[^\d+]", "", phone)

    if len(re.sub(r"\D", "", phone)) < 8:
        return None

    return phone


def extract_name(text: str, phone: str | None) -> str | None:
    if not phone:
        return None

    name_part = text.replace(phone, "").strip(" ,.-\n")
    if not name_part:
        return None

    return name_part


@router.message()
async def process_text_message(
    message: Message,
    container: ServiceContainer,
) -> None:
    if not message.text:
        return

    if message.chat.type != "private":
        return

    conversation = container.conversations.get_or_create(message.from_user.id)
    text = message.text.strip()

    if conversation.stage == "contact_capture":
        phone = extract_phone(text)
        name = extract_name(text, phone)

        if not phone:
            await message.answer(
                "Не вдалося розпізнати номер телефону. "
                "Надішліть, будь ласка, ім’я та номер одним повідомленням.\n\n"
                "Приклад:\n"
                "Іван +380501234567"
            )
            return

        operator_text = (
            "<b>Новий запит на контакт</b>\n"
            f"Користувач: {message.from_user.full_name}\n"
            f"username: @{message.from_user.username if message.from_user.username else '-'}\n"
            f"user_id: <code>{message.from_user.id}</code>\n"
            f"Ім’я: {name or '-'}\n"
            f"Телефон: <code>{phone}</code>\n\n"
            f"<b>Повідомлення клієнта:</b>\n{text}"
        )

        await message.bot.send_message(
            chat_id=container.handoff.operator_chat_id,
            text=operator_text,
        )

        container.conversations.update_stage(message.from_user.id, "contact_captured")
        container.conversations.set_mode(message.from_user.id, "handoff_requested")

        await message.answer(
            "Дякую! Я передав ваші контактні дані менеджеру. "
            "З вами зв’яжуться найближчим часом."
        )
        return

    if conversation.mode == "handoff_requested":
        await container.handoff.forward_client_message_to_operator_group(message)
        return

    if conversation.mode == "human":
        await container.handoff.forward_client_message_to_operator_group(message)
        return

    if conversation.mode == "closed":
        container.conversations.back_to_bot(message.from_user.id)
        await message.answer(
            "Діалог було завершено. За потреби можете поставити нове запитання.",
            reply_markup=main_menu_keyboard(),
        )
        return

    decision = await container.router_service.route(message.from_user.id, text)

    if decision.action == "handoff":
        await container.handoff.request_operator(message, reason=decision.reason)
        return

    if decision.action == "faq":
        await message.answer(
            decision.reply,
            reply_markup=main_menu_keyboard(),
        )
        return

    if decision.action == "collect_contact":
        container.conversations.update_stage(message.from_user.id, "contact_capture")
        await message.answer(
            container.dialogs.contact_request_text()
            + "\n\nПриклад:\nІван +380501234567"
        )
        return

    if decision.action == "ai_reply" and decision.reply:
        await message.answer(
            decision.reply,
            reply_markup=main_menu_keyboard(),
        )
        return

    await message.answer(
        container.dialogs.fallback_text(),
        reply_markup=main_menu_keyboard(),
    )