from api.client import BotApiClient
from api.models import TicketMessage, TicketMessageCreateBody, Ticket, TicketCreateBody, ObjectCreateResponse
from core.api.client import ApiClient
from core.api.models import PaginatedRetrieveQuery, PaginatedResult, PageQuery, RetrieveQuery

from settings import Settings

settings = Settings()

client = ApiClient(
    base_url=settings.base_api_url,
    headers={
        "X-Telegram-Bot-Api-Token": str(settings.bot_api_token),
    }
)

client.register_endpoint(
    name="get_ticket_messages",
    path="tickets/ticket_messages/{id}/list_messages_for_ticket/",
    query_validator=PaginatedRetrieveQuery,
    response_validator=PaginatedResult[TicketMessage],
    method="GET"
)
client.register_endpoint(
    name="create_ticket_message",
    path="tickets/ticket_messages/",
    body_validator=TicketMessageCreateBody,
    method="POST"
)
client.register_endpoint(
    name="get_tickets",
    path="tickets/tickets/",
    query_validator=PageQuery,
    response_validator=PaginatedResult[Ticket],
    method="GET"
)
client.register_endpoint(
    name="create_ticket",
    path="tickets/tickets/",
    body_validator=TicketCreateBody,
    response_validator=ObjectCreateResponse,
    method="POST"
)
client.register_endpoint(
    name="get_ticket",
    path="tickets/tickets/{id}",
    query_validator=RetrieveQuery,
    response_validator=Ticket,
    method="GET"
)
client.register_endpoint(
    name="close_ticket",
    path="tickets/tickets/{id}/close_ticket/",
    query_validator=RetrieveQuery,
    method="POST"
)

bot_api = BotApiClient(client)
