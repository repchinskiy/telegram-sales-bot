from dataclasses import dataclass

from app.repositories.conversation_repository import ConversationRepository
from app.repositories.message_bridge_repository import MessageBridgeRepository
from app.services.ai_service import AIService
from app.services.dialog_service import DialogService
from app.services.handoff_service import HandoffService
from app.services.routing_service import RoutingService


@dataclass
class ServiceContainer:
    conversations: ConversationRepository
    bridge: MessageBridgeRepository
    dialogs: DialogService
    ai_service: AIService
    router_service: RoutingService
    handoff: HandoffService

    @classmethod
    def from_settings(cls, settings):
        conversations = ConversationRepository()
        bridge = MessageBridgeRepository()
        dialogs = DialogService()
        ai_service = AIService(enabled=settings.use_ai)
        router_service = RoutingService(dialogs, ai_service, conversations)
        handoff = HandoffService(
            settings.operator_chat_id,
            conversations,
            dialogs,
            bridge,
        )

        return cls(
            conversations=conversations,
            bridge=bridge,
            dialogs=dialogs,
            ai_service=ai_service,
            router_service=router_service,
            handoff=handoff,
        )