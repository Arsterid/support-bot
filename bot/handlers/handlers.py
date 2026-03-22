from typing import Optional
from aiogram_dialog import DialogManager

PAGE_SIZE = 5


def create_pagination_handlers(prefix: str, affix: Optional[str] = None):
    async def on_prev(_, __, manager: DialogManager):
        key = f"{prefix}_page"

        if isinstance(affix, str):
            affix_data = manager.dialog_data[affix]
            key = f"{prefix}_page_{affix_data}"

        page = int(manager.dialog_data.get(key, 1))
        manager.dialog_data[key] = max(1, page - 1)
        await manager.show()

    async def on_next(_, __, manager: DialogManager):
        key = f"{prefix}_page"

        if isinstance(affix, str):
            affix_data = manager.dialog_data[affix]
            key = f"{prefix}_page_{affix_data}"

        page = int(manager.dialog_data.get(key, 1))
        manager.dialog_data[key] = page + 1
        await manager.show()

    return on_prev, on_next
