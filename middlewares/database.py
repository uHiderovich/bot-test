import logging
from typing import Any, Awaitable, Callable

from aiogram import BaseMiddleware
from aiogram.types import Update
from psycopg_pool import AsyncConnectionPool

logger = logging.getLogger(__name__)


class DataBaseMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[Update, dict[str, Any]], Awaitable[Any]],
        event: Update,
        data: dict[str, Any],
    ) -> Any:
        db_pool: AsyncConnectionPool = data.get("db_pool")

        if db_pool is None:
            logger.error("Database pool is not provided in middleware data.")
            raise RuntimeError("Missing db_pool in middleware context.")

        async with db_pool.connection() as connection:
            try:
                async with connection.transaction():
                    data["conn"] = connection
                    result = await handler(event, data)
            except Exception as e:
                logger.exception("Transaction rolled back due to error: %s", e)
                raise

        # Здесь может быть какой-то код, который выполнится в случае успешного завершения транзакции

        return result
