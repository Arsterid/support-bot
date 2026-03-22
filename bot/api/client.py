from typing import Optional, Awaitable


class BotApiClient:
    def __init__(self, client):
        self.client = client

    def _form_auth_header_for_user(self, user_id: int):
        return {"X-Telegram-User-Id": str(user_id)}

    def _get_default_headers(self, **kwargs):
        headers = {}

        user_id = kwargs.get("user_id")
        if isinstance(user_id, int):
            headers.update(self._form_auth_header_for_user(user_id))

        return headers

    def _get_client_method(self, method: str) -> callable:
        method = getattr(self.client, method)
        assert callable(method), "Client has not implemented method {}".format(method)
        return method

    def _request(
            self,
            user_id: int,
            method_name: str,
            *,
            headers: Optional[dict] = None,
            body: Optional[dict] = None,
            query_params: Optional[dict] = None
    ) -> Awaitable:
        default_headers = self._get_default_headers(user_id=user_id)
        headers = {**default_headers, **headers}

        method = self._get_client_method(method_name)
        return method(headers=headers, body=body, query_params=query_params)

    # Ticket

    async def get_ticket(self, user_id: int, ticket_id: int):
        return self._request(user_id, "get_ticket", query_params={
            "pk": ticket_id
        })

    async def get_tickets(self, user_id: int, page: int = 1):
        return self._request(user_id, "get_tickets", query_params={
            "page": page,
        })

    async def create_ticket(self, user_id: int, name: str):
        return self._request(user_id, "create_ticket", body={"name": name})

    async def close_ticket(self, user_id: int, ticket_id: int):
        return self._request(user_id, "close_ticket", query_params={"pk": ticket_id})

    # Ticket messages

    async def get_ticket_messages(self, user_id: int, ticket_id: int, page: int = 1):
        return self._request(user_id, "get_ticket_messages", query_params={
            "page": page,
            "pk": ticket_id
        })

    async def create_ticket_message(self, user_id: int, ticket_id: int, text: str):
        return self._request(user_id, "create_ticket_message", body={
            "text": text,
            "ticket": ticket_id
        })
