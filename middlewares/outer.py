import logging
from typing import Any, Awaitable, Callable, Dict

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject

logger = logging.getLogger(__name__)


class FirstOuterMiddleware(BaseMiddleware):

    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any],
    ) -> Any:

        logger.debug(
            "Вошли в миддлварь %s, тип события %s",
            self.__class__.__name__,
            event.__class__.__name__,
        )

        # logger.debug("Выходим из миддлвари  %s", self.__class__.__name__)

        # Вместо `result = await handler(event, data)` пишем `return` и,
        # соответственно, код после return выполняться тоже не будет
        # return

        result = await handler(event, data)

        logger.debug("Выходим из миддлвари  %s", self.__class__.__name__)

        return result


class SecondOuterMiddleware(BaseMiddleware):

    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any],
    ) -> Any:

        logger.debug(
            "Вошли в миддлварь %s, тип события %s",
            self.__class__.__name__,
            event.__class__.__name__,
        )

        result = await handler(event, data)

        logger.debug("Выходим из миддлвари  %s", self.__class__.__name__)

        return result


class ThirdOuterMiddleware(BaseMiddleware):

    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any],
    ) -> Any:

        logger.debug(
            "Вошли в миддлварь %s, тип события %s",
            self.__class__.__name__,
            event.__class__.__name__,
        )

        result = await handler(event, data)

        logger.debug("Выходим из миддлвари  %s", self.__class__.__name__)

        return result
