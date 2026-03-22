from typing import Any

from aiogram_dialog import DialogManager

from api import bot_api, ObjectCreateResponse, Ticket
from core.api.models import PaginatedResult
from states import BotStates


async def close_ticket(_: Any, __: Any, manager: DialogManager):
    user_id = manager.event.from_user.id
    ticket_id = manager.dialog_data["ticket_id"]

    response = await bot_api.close_ticket(user_id, ticket_id)

    await manager.switch_to(BotStates.TICKETS_LIST)


async def create_new_ticket(_: Any, __: Any, manager: DialogManager, ticket_name: str):
    ticket_name = ticket_name.strip()
    user_id = manager.event.from_user.id

    response: ObjectCreateResponse = await bot_api.create_ticket(user_id, ticket_name)
    ticket_id = response.id
    manager.dialog_data["ticket_id"] = ticket_id

    await manager.switch_to(BotStates.VIEW_TICKET)


async def on_select_ticket(_: Any, __: Any, manager: DialogManager, item_id: str):
    manager.dialog_data["ticket_id"] = int(item_id)
    await manager.switch_to(BotStates.VIEW_TICKET)


async def tickets_getter(dialog_manager: DialogManager, **_):
    page = int(dialog_manager.dialog_data.get("tickets_list_page", 1))
    user_id = dialog_manager.event.from_user.id
    api_page: PaginatedResult[Ticket] = await bot_api.get_tickets(user_id, page)

    return {
        "page": page,
        "pages": api_page.max_pages,
        "count": api_page.count,
        "has_prev": api_page.previous is not None,
        "has_next": api_page.next is not None,
        "tickets": [t.model_dump() for t in api_page.results],
    }
