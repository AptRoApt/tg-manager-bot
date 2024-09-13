from bot.utils.store import Store, User
from typing import Callable, Dict, Any, Awaitable
from aiogram import BaseMiddleware
from aiogram.types import Message, CallbackQuery


class UpdateUserInfoMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[Message | CallbackQuery, Dict[str, Any]], Awaitable[Any]],
        event: Message | CallbackQuery,
        data: Dict[str, Any]
    ) -> Any:
        store: Store = data.get("store")
        store.add_user(User(id=event.from_user.id,
                       username=event.from_user.username,
                       first_name=event.from_user.first_name,
                       chat_id=event.chat.id))
        return await handler(event, data)
