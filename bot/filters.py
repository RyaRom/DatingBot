from aiogram.types import Message


class AdminFilter:
    def __init__(self, admin_ids: list[int]):
        self.admin_ids = admin_ids

    def __call__(self, message: Message, **kwargs):
        return message.from_user.id in self.admin_ids
