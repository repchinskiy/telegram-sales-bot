from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

from app.config import settings
from app.handlers import register_handlers
from app.services.container import ServiceContainer


async def main() -> None:
    bot = Bot(
        token=settings.bot_token,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML),
    )

    dp = Dispatcher()
    container = ServiceContainer.from_settings(settings)

    register_handlers(dp)
    await dp.start_polling(bot, container=container)