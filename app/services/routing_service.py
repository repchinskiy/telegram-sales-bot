from app.schemas.routing import RoutingDecision


class RoutingService:
    def __init__(self, dialogs, ai_service, conversations) -> None:
        self.dialogs = dialogs
        self.ai_service = ai_service
        self.conversations = conversations

    async def route(self, user_id: int, text: str) -> RoutingDecision:
        normalized = text.lower().strip()

        human_request_phrases = [
            "оператор",
            "менеджер",
            "людина",
            "человек",
            "живий менеджер",
            "живой менеджер",
            "жива людина",
            "свяжите с менеджером",
            "зв'яжіть з менеджером",
            "передайте менеджеру",
            "соедините с оператором",
            "хочу с человеком",
            "хочу поговорить с менеджером",
            "переключите на оператора",
        ]

        hot_lead_phrases = [
            "хочу купити",
            "хочу купить",
            "хочу замовити",
            "хочу заказать",
            "готовий оплатити",
            "готов оплатить",
            "готов оформить",
            "хочу оформити",
            "хочу оформити замовлення",
            "потрібен рахунок",
            "нужен счет",
            "нужен договор",
            "потрібен договір",
            "хочу підключити",
            "хочу подключить",
            "коли можна підключити",
            "когда можно подключить",
            "можна замовити",
            "можно заказать",
        ]

        callback_request_phrases = [
            "передзвоніть",
            "перезвоните",
            "зателефонуйте",
            "позвоните",
            "зв'яжіться зі мною",
            "свяжитесь со мной",
            "мій номер",
            "мой номер",
            "можу залишити номер",
            "могу оставить номер",
        ]

        urgent_phrases = [
            "терміново",
            "срочно",
            "якнайшвидше",
            "как можно быстрее",
            "сьогодні",
            "сегодня",
            "прямо зараз",
            "прямо сейчас",
        ]

        faq_price_phrases = [
            "ціна",
            "ціни",
            "вартість",
            "скільки коштує",
            "скільки буде",
            "price",
            "цена",
            "стоимость",
            "сколько стоит",
        ]

        faq_legal_phrases = [
            "рахунок",
            "счет",
            "договір",
            "договор",
            "закриваючі документи",
            "закрывающие документы",
            "юрособа",
            "юрлицо",
            "фоп",
            "оплата по безналу",
            "безнал",
        ]

        faq_battery_phrases = [
            "батарея",
            "батареї",
            "акумулятор",
            "акумулятори",
            "инвертор",
            "інвертор",
            "резервне живлення",
            "резервное питание",
        ]

        if any(phrase in normalized for phrase in human_request_phrases):
            return RoutingDecision(action="handoff", reason="user_requested_human")

        if any(phrase in normalized for phrase in hot_lead_phrases):
            return RoutingDecision(action="handoff", reason="hot_lead")

        if any(phrase in normalized for phrase in callback_request_phrases):
            return RoutingDecision(action="collect_contact")

        if any(phrase in normalized for phrase in urgent_phrases):
            return RoutingDecision(action="handoff", reason="urgent_request")

        if any(phrase in normalized for phrase in faq_price_phrases):
            return RoutingDecision(
                action="faq",
                reply=self.dialogs.match_faq("ціна") or
                "Вартість залежить від конфігурації та форми оплати. Можу передати ваш запит менеджеру для точного розрахунку.",
            )

        if any(phrase in normalized for phrase in faq_legal_phrases):
            return RoutingDecision(
                action="faq",
                reply=self.dialogs.match_faq("договір") or
                "Для юридичних осіб можемо підготувати рахунок і необхідні документи.",
            )

        if any(phrase in normalized for phrase in faq_battery_phrases):
            return RoutingDecision(
                action="faq",
                reply=self.dialogs.match_faq("інвертор") or
                "Щоб підготувати предметну відповідь, уточніть потужність, бажаний бренд і сценарій використання.",
            )

        faq_reply = self.dialogs.match_faq(normalized)
        if faq_reply:
            return RoutingDecision(action="faq", reply=faq_reply)

        ai_reply = await self.ai_service.reply(text)
        if ai_reply:
            return RoutingDecision(action="ai_reply", reply=ai_reply)

        return RoutingDecision(action="fallback")