from dataclasses import dataclass


@dataclass
class RoutingDecision:
    action: str
    reply: str | None = None
    reason: str | None = None