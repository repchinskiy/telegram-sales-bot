class AIService:
    def __init__(self, enabled: bool = False) -> None:
        self.enabled = enabled

    async def reply(self, text: str) -> str | None:
        if not self.enabled:
            return None
        return (
            "Понял ваш запрос. Я могу дать предварительный ответ, "
            "но для точного расчета лучше подключить менеджера. "
            f"Ваш вопрос: {text}"
        )