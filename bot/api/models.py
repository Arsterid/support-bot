from typing import Optional, List

from pydantic import BaseModel


# TODO rewrite to T

class User(BaseModel):
    id: int
    username: str
    telegram_user_id: Optional[int]
    auth_source: str
    is_tg_auth: bool


class TicketMessage(BaseModel):
    id: int
    user: User
    text: str
    ticket: int

    created_at: str


class Ticket(BaseModel):
    id: int
    user: User
    processed_by: List[User]
    name: str
    status: int
    is_open: bool

    created_at: str
    updated_at: str


class TicketMessageCreateBody(BaseModel):
    text: str
    ticket: int


class TicketCreateBody(BaseModel):
    name: str


class ObjectCreateResponse(BaseModel):
    id: int
