from aiogram.types import CallbackQuery, Message

from app.keyboards.operator_actions import (
    operator_active_keyboard,
    operator_request_keyboard,
)


class HandoffService:
    def __init__(self, operator_chat_id: int, conversations, dialogs, bridge) -> None:
        self.operator_chat_id = operator_chat_id
        self.conversations = conversations
        self.dialogs = dialogs
        self.bridge = bridge

    async def request_operator(self, message: Message, reason: str) -> None:
        user = message.from_user

        self.conversations.set_mode(user.id, "handoff_requested")
        self.conversations.update_stage(user.id, "handoff_requested")

        operator_text = (
            "<b>Нове звернення на оператора</b>\n"
            f"Причина: {reason}\n"
            f"Користувач: {user.full_name}\n"
            f"username: @{user.username if user.username else '-'}\n"
            f"user_id: <code>{user.id}</code>\n\n"
            f"<b>Повідомлення клієнта:</b>\n{message.text}"
        )

        sent = await message.bot.send_message(
            chat_id=self.operator_chat_id,
            text=operator_text,
            reply_markup=operator_request_keyboard(user.id),
        )

        self.bridge.bind(sent.message_id, user.id)

        conversation = self.conversations.get_or_create(user.id)
        conversation.operator_request_message_id = sent.message_id

        await message.answer(self.dialogs.operator_wait_text())

    async def request_operator_from_callback(
        self,
        callback: CallbackQuery,
        reason: str,
    ) -> None:
        user = callback.from_user

        self.conversations.set_mode(user.id, "handoff_requested")
        self.conversations.update_stage(user.id, "handoff_requested")

        operator_text = (
            "<b>Нове звернення на оператора</b>\n"
            f"Причина: {reason}\n"
            f"Користувач: {user.full_name}\n"
            f"username: @{user.username if user.username else '-'}\n"
            f"user_id: <code>{user.id}</code>\n\n"
            "<b>Джерело звернення:</b>\n"
            "Користувач натиснув кнопку «Покликати оператора»."
        )

        sent = await callback.bot.send_message(
            chat_id=self.operator_chat_id,
            text=operator_text,
            reply_markup=operator_request_keyboard(user.id),
        )

        self.bridge.bind(sent.message_id, user.id)

        conversation = self.conversations.get_or_create(user.id)
        conversation.operator_request_message_id = sent.message_id

        await callback.message.answer(self.dialogs.operator_wait_text())
        await callback.answer()

    async def forward_client_message_to_operator_group(self, message: Message) -> None:
        user = message.from_user
        conversation = self.conversations.get_or_create(user.id)

        operator_text = (
            "<b>Нове повідомлення від клієнта</b>\n"
            f"Користувач: {user.full_name}\n"
            f"username: @{user.username if user.username else '-'}\n"
            f"user_id: <code>{user.id}</code>\n"
            f"Оператор: <code>{conversation.assigned_operator_id or '-'}</code>\n\n"
            f"{message.text}"
        )

        sent = await message.bot.send_message(
            chat_id=self.operator_chat_id,
            text=operator_text,
            reply_markup=operator_active_keyboard(user.id),
        )

        self.bridge.bind(sent.message_id, user.id)

    async def send_operator_reply_to_client(
        self,
        operator_message: Message,
        client_user_id: int,
    ) -> None:
        await operator_message.bot.send_message(
            chat_id=client_user_id,
            text=operator_message.text,
        )