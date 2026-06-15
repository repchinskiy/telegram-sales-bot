class MessageBridgeRepository:
    def __init__(self) -> None:
        self._group_to_client: dict[int, int] = {}

    def bind(self, group_message_id: int, client_user_id: int) -> None:
        self._group_to_client[group_message_id] = client_user_id

    def get_client_id(self, group_message_id: int) -> int | None:
        return self._group_to_client.get(group_message_id)