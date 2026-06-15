from datetime import datetime

from app.schemas.conversation import Conversation


class ConversationRepository:
    def __init__(self) -> None:
        self._storage: dict[int, Conversation] = {}

    def get_or_create(self, user_id: int) -> Conversation:
        conversation = self._storage.get(user_id)
        if conversation is None:
            conversation = Conversation(user_id=user_id)
            self._storage[user_id] = conversation
        return conversation

    def get(self, user_id: int) -> Conversation | None:
        return self._storage.get(user_id)

    def update_stage(self, user_id: int, stage: str) -> Conversation:
        conversation = self.get_or_create(user_id)
        conversation.stage = stage
        conversation.updated_at = datetime.utcnow()
        return conversation

    def set_mode(self, user_id: int, mode: str) -> Conversation:
        conversation = self.get_or_create(user_id)
        conversation.mode = mode
        conversation.updated_at = datetime.utcnow()
        return conversation

    def assign_operator(
        self,
        user_id: int,
        operator_id: int,
        request_message_id: int | None = None,
    ) -> Conversation:
        conversation = self.get_or_create(user_id)
        conversation.assigned_operator_id = operator_id
        conversation.operator_request_message_id = request_message_id
        conversation.mode = "human"
        conversation.stage = "human"
        conversation.updated_at = datetime.utcnow()
        return conversation

    def close(self, user_id: int) -> Conversation:
        conversation = self.get_or_create(user_id)
        conversation.mode = "closed"
        conversation.stage = "closed"
        conversation.assigned_operator_id = None
        conversation.updated_at = datetime.utcnow()
        return conversation

    def back_to_bot(self, user_id: int) -> Conversation:
        conversation = self.get_or_create(user_id)
        conversation.mode = "bot"
        conversation.stage = "welcome"
        conversation.assigned_operator_id = None
        conversation.updated_at = datetime.utcnow()
        return conversation