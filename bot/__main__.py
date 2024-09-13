from aiogram import Bot, Dispatcher, F
import asyncio
from aiogram.client.default import DefaultBotProperties
import logging
from bot.config import Config
from bot.middlewares.update_user_info import UpdateUserInfoMiddleware
from bot.utils.store import Store


async def main():
    # Настройка основных сущностей
    logging.basicConfig(level=logging.INFO)
    config = Config()
    store = Store(config.db_path)
    bot = Bot(token=config.bot_token,
              default=DefaultBotProperties(parse_mode="HTML"))
    dp = Dispatcher(store=store, admin_id=config.admin_id)

    # Подключение фильтров
    dp.message.filter(F.chat.type == "private")
    dp.message.middleware(UpdateUserInfoMiddleware())

    # Подключение роутеров
    from bot.handlers.admin import admin_router
    from bot.handlers.users import users_router
    dp.include_routers(admin_router, users_router)

    # Задание меню
    # ...

    try:
        await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())
    finally:
        await bot.session.close()
        store.close()

if __name__ == '__main__':
    asyncio.run(main())
