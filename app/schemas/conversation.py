from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class Conversation:
    user_id: int
    stage: str = "welcome"
    mode: str = "bot"
    lead_score: int = 0
    assigned_operator_id: int | None = None
    operator_request_message_id: int | None = None
    created_at: datetime = field(default_factory=datetime.utcnow)
    updated_at: datetime = field(default_factory=datetime.utcnow)