from aiogram import Router
from aiogram.types import Message
from aiogram.filters.command import CommandStart, Command
from bot.utils.store import Store
users_router = Router()


@users_router.message(CommandStart())
@users_router.message(Command("help"))
async def cmd_start(message: Message, store: Store):
    msg_text = "Здравствуйте! Смело пишите сюда все свои предложения, проблемы и вопросы. Мы обязательно поможем."
    await message.answer(msg_text)

# Можно отправить чужое сообщщщщение и эт овсё сломает.
@users_router.message()
async def send_to_admin(message: Message, store: Store, admin_id: int):
    admin = store.get_user_by_id(user_id=admin_id)
    if not admin:
        await message.reply("К сожалению, бот ещё не настроен. Попробуйте позже.")
        return
    if message.forward_from and message.forward_from.id != message.from_user.id:
        await message.reply(("Вы не можете отправлять сообщения от чужого имени.\n"
                             "Вы можете скрыть имя отправителя, чтобы переслать чужое сообщение."))
        return
    await message.bot.send_message(chat_id=admin.chat_id, text=f"Сообщение от {message.from_user.username}")
    await message.forward(chat_id=admin.chat_id)

