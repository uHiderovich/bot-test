import asyncio
import logging
import os
import sys
import psycopg_pool

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.fsm.storage.redis import RedisStorage

from redis.asyncio import Redis

from handlers.admin import admin_router
from handlers.others import others_router
from handlers.settings import settings_router
from handlers.user import user_router
from i18n.translator import get_translations
from middlewares.database import DataBaseMiddleware
from middlewares.i18n import TranslatorMiddleware
from middlewares.lang_settings import LangSettingsMiddleware
from middlewares.shadow_ban import ShadowBanMiddleware
from middlewares.statistics import ActivityCounterMiddleware
from database.connection import get_pg_pool
from config_data.config import Config, load_config

config: Config = load_config()

logging.basicConfig(
    level=logging.getLevelName(level=config.log.level),
    format=config.log.format,
)

if sys.platform.startswith("win") or os.name == "nt":
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())


logger = logging.getLogger(__name__)


# Функция конфигурирования и запуска бота
async def main(config: Config) -> None:
    logger.info("Starting bot...")
    # Инициализируем хранилище
    storage = RedisStorage(
        redis=Redis(
            host=config.redis.host,
            port=config.redis.port,
            db=config.redis.db,
            password=config.redis.password,
            username=config.redis.username,
        )
    )

    # Инициализируем бот и диспетчер
    bot = Bot(
        token=config.bot.token,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML),
    )
    dp = Dispatcher(storage=storage)

    # Создаём пул соединений с Postgres
    db_pool: psycopg_pool.AsyncConnectionPool = await get_pg_pool(
        db_name=config.db.name,
        host=config.db.host,
        port=config.db.port,
        user=config.db.user,
        password=config.db.password,
    )

    # Получаем словарь с переводами
    translations = get_translations()
    # формируем список локалей из ключей словаря с переводами
    locales = list(translations.keys())

    # Подключаем роутеры в нужном порядке
    logger.info("Including routers...")
    dp.include_routers(settings_router, admin_router, user_router, others_router)

    # Подключаем миддлвари в нужном порядке
    logger.info("Including middlewares...")
    dp.update.middleware(DataBaseMiddleware())
    dp.update.middleware(ShadowBanMiddleware())
    dp.update.middleware(ActivityCounterMiddleware())
    dp.update.middleware(LangSettingsMiddleware())
    dp.update.middleware(TranslatorMiddleware())

    # Запускаем поллинг
    try:
        await dp.start_polling(
            bot,
            db_pool=db_pool,
            translations=translations,
            locales=locales,
            admin_ids=config.bot.admin_ids,
        )
    except Exception as e:
        logger.exception(e)
    finally:
        # Закрываем пул соединений
        await db_pool.close()
        logger.info("Connection to Postgres closed")


asyncio.run(main(config))
