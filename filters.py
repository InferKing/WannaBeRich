from aiogram.filters import BaseFilter
from aiogram.types import Message
from db import find_user_by_id


class RegisterUserFilter(BaseFilter):
    async def __call__(self, message: Message) -> bool:
        return bool(await find_user_by_id(message.from_user.id))


class UnregisterUserFilter(BaseFilter):
    async def __call__(self, message: Message) -> bool:
        return not bool(await find_user_by_id(message.from_user.id))