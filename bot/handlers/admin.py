from aiogram import Router, F
from aiogram.types import Message
from aiogram.exceptions import TelegramForbiddenError
from bot.utils.store import Store, User
from bot.handlers.users import send_to_admin

admin_router = Router()


@admin_router.message(F.reply_to_message)
async def send_to_user(message: Message, store: Store, admin_id: int):
    if message.from_user.id != admin_id:
        send_to_admin(message, store, admin_id)
    receiver_id = message.reply_to_message.forward_from.id
    reciever: User = store.get_user_by_id(receiver_id)
    try:
        await message.copy_to(chat_id = reciever.chat_id)
    except TelegramForbiddenError:
        await message.answer(f"Пользователь запретил сообщения от бота.")
    except Exception as e:
        await message.answer(f"Неизвестная ошибка: {e}")
