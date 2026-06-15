from config.dialogs import DIALOGS, FAQ_ANSWERS


class DialogService:
    def welcome_text(self) -> str:
        return DIALOGS["welcome"]

    def tariffs_text(self) -> str:
        return DIALOGS["tariffs"]

    def connection_text(self) -> str:
        return DIALOGS["connection"]

    def consultation_text(self) -> str:
        return DIALOGS["consultation"]

    def operator_wait_text(self) -> str:
        return DIALOGS["operator_wait"]

    def contact_request_text(self) -> str:
        return DIALOGS["contact_request"]

    def fallback_text(self) -> str:
        return DIALOGS["fallback"]

    def match_faq(self, text: str) -> str | None:
        normalized = text.lower()
        if any(word in normalized for word in ["цена", "стоимость", "сколько"]):
            return FAQ_ANSWERS["price"]
        if any(word in normalized for word in ["юр", "договор", "счет", "счёт", "фоп"]):
            return FAQ_ANSWERS["legal"]
        if any(word in normalized for word in ["батар", "інвертор", "инвертор", "акум"]):
            return FAQ_ANSWERS["battery"]
        return None