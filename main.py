import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from config_data.config import Config, load_config

# Импортируем роутеры
# ...
# Импортируем миддлвари
# ...
# Импортируем вспомогательные функции для создания нужных объектов
# ...
from keyboards.set_menu import set_main_menu

# Инициализируем логгер
logger = logging.getLogger(__name__)


# Функция конфигурирования и запуска бота
async def main():
    # Конфигурируем логирование
    logging.basicConfig(
        level=logging.INFO,
        format="%(filename)s:%(lineno)d #%(levelname)-8s "
        "[%(asctime)s] - %(name)s - %(message)s",
    )

    # Выводим в консоль информацию о начале запуска бота
    logger.info("Starting bot")

    # Загружаем конфиг в переменную config
    config: Config = load_config()

    # Инициализируем объект хранилища
    storage = None

    # Инициализируем бот и диспетчер
    bot = Bot(
        token=config.tg_bot.token,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML),
    )
    dp = Dispatcher(storage=storage)

    # Инициализируем другие объекты (пул соединений с БД, кеш и т.п.)
    # ...

    # Помещаем нужные объекты в workflow_data диспетчера
    # dp.workflow_data.update(...)

    # Настраиваем главное меню бота
    await set_main_menu(bot)

    dp.startup.register(set_main_menu)

    # Регистриуем роутеры
    logger.info("Подключаем роутеры")
    # ...

    # Регистрируем миддлвари
    logger.info("Подключаем миддлвари")
    # ...

    @dp.message(Command(commands="delmenu"))
    async def del_main_menu(message: Message, bot: Bot):
        await bot.delete_my_commands()
        await message.answer(text='Кнопка "Menu" удалена')

    # Пропускаем накопившиеся апдейты и запускаем polling
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


asyncio.run(main())
