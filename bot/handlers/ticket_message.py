from typing import Any, List

from aiogram_dialog import DialogManager

from api import ObjectCreateResponse, bot_api, TicketMessage, Ticket
from core.api.models import PaginatedResult
from core.utils.utils import parse_date
from states import BotStates


async def create_new_ticket_message(_: Any, __: Any, manager: DialogManager, message_text: str):
    message_text = message_text.strip()
    user_id = manager.event.from_user.id

    ticket_id = manager.dialog_data["ticket_id"]

    response: ObjectCreateResponse = await bot_api.create_ticket_message(user_id, ticket_id, message_text)

    await manager.switch_to(BotStates.VIEW_TICKET)


def form_message(ticket_messages: List[TicketMessage], user_name: str, user_id: int):
    result = []
    for message in ticket_messages:
        name = message.user.username if not message.user.telegram_user_id == user_id else f'@{user_name}'
        result.append(
            f"{name} | {parse_date(message.created_at)}\n"
            f"{message.text}\n"
        )
    return result


async def ticket_messages_getter(dialog_manager: DialogManager, **_):
    ticket_id = dialog_manager.dialog_data["ticket_id"]

    page = int(dialog_manager.dialog_data.get(f"ticket_view_page_{ticket_id}", 1))

    user = dialog_manager.event.from_user
    user_id = user.id
    ticket_data: Ticket = await bot_api.get_ticket(user_id, ticket_id)
    messages_api_page: PaginatedResult[TicketMessage] = await bot_api.get_ticket_messages(user_id, ticket_id, page)

    user_name = user.username
    messages = form_message(messages_api_page.results, user_name, user_id)

    return {
        "page": page,
        "pages": messages_api_page.max_pages,
        "count": messages_api_page.count,
        "has_prev": messages_api_page.previous is not None,
        "has_next": messages_api_page.next is not None,
        "name": ticket_data.name,
        "is_open": ticket_data.is_open,
        "messages": "\n".join(messages) or "---\n"
    }
