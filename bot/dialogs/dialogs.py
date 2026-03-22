from typing import Optional

from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.input import TextInput
from aiogram_dialog.widgets.text import Const, Format, Multi, Case
from aiogram_dialog.widgets.kbd import Button, Row, Select, Column, SwitchTo

from handlers.handlers import create_pagination_handlers
from handlers.ticket import close_ticket, create_new_ticket, on_select_ticket, tickets_getter
from handlers.ticket_message import create_new_ticket_message, ticket_messages_getter
from states import BotStates
from texts import Texts


def create_pager(
        prefix: str,
        affix: Optional[str] = None,
        previous_field: Optional[str] = "has_prev",
        next_field: [str] = "has_next"
):
    on_prev, on_next = create_pagination_handlers(prefix, affix)

    pager = Row(
        Button(Format(Texts.PREV), id="prev", on_click=on_prev, when=previous_field),
        Button(Format(Texts.NEXT), id="next", on_click=on_next, when=next_field),
    )

    return pager


start_window = Window(
    Const(Texts.WELCOME),
    SwitchTo(Const(Texts.NEW_TICKET), id="new_ticket", state=BotStates.NEW_TICKET),
    SwitchTo(Const(Texts.VIEW_TICKETS), id="my_tickets", state=BotStates.TICKETS_LIST),
    state=BotStates.MAIN,
)


ticket_list_window = Window(
    Format(
        f"{Texts.TICKETS_TITLE}\n"
        f"{Texts.TOTAL}: {{count}}\n"
        f"{Texts.PAGE}: {{page}}/{{pages}}\n"
    ),
    Column(
        Select(
            text=Multi(
                Case(
                    texts={
                        True: Const('⚙️'),
                        False: Const('🔒'),
                    },
                    selector=lambda data, widget, manager: bool(data.get('item', {}).get('is_open', False)),
                ),
                Const(' '),
                Format('{item[name]}'),
            ),
            id="ticket_select",
            items="tickets",
            item_id_getter=lambda item: str(item["id"]),
            on_click=on_select_ticket,
        ),
    ),
    create_pager("tickets_list"),
    SwitchTo(Const(Texts.NEW_TICKET), id="new_ticket", state=BotStates.MAIN),
    state=BotStates.TICKETS_LIST,
    getter=tickets_getter,
)

new_ticket_window = Window(
    Const(Texts.ENTER_TICKET_NAME),
    TextInput(
        id="new_ticket",
        on_success=create_new_ticket,
    ),
    SwitchTo(Const(Texts.NEW_TICKET), id="new_ticket", state=BotStates.MAIN),
    state=BotStates.NEW_TICKET,
)

view_ticket_window = Window(
    Format(
        f"{Texts.TICKET_NAME}: {{name}}\n"
        f"{Texts.MESSAGE_HISTORY}: \n\n"
        f"{{messages}}\n"
        f"{Texts.PAGE}: {{page}}/{{pages}}\n"
    ),
    create_pager("ticket_view", "ticket_id"),
    Button(Const(Texts.CLOSE_TICKET), id="close_ticket", on_click=close_ticket, when="is_open"),
    SwitchTo(Const(Texts.NEW_MESSAGE), id="new_ticket", state=BotStates.NEW_MESSAGE, when="is_open"),
    SwitchTo(Const(Texts.BACK), id="new_ticket", state=BotStates.TICKETS_LIST),
    state=BotStates.VIEW_TICKET,
    getter=ticket_messages_getter
)

new_message_window = Window(
    Const(Texts.ENTER_MESSAGE_TEXT),
    TextInput(
        id="new_message",
        on_success=create_new_ticket_message
    ),
    SwitchTo(Const(Texts.BACK), id="back", state=BotStates.VIEW_TICKET),
    state=BotStates.NEW_MESSAGE,
)

dialog = Dialog(
    start_window,
    ticket_list_window,
    new_ticket_window,
    view_ticket_window,
    new_message_window,
)
