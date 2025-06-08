import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart

from aiogram.types import Message
from config_data.config import Config, load_config

from keyboards.create_inline_kb import create_inline_kb


# Инициализируем логгер
logger = logging.getLogger(__name__)


BUTTONS: dict[str, str] = {
    "btn_1": "1",
    "btn_2": "2",
    "btn_3": "3",
    "btn_4": "4",
    "btn_5": "5",
    "btn_6": "6",
    "btn_7": "7",
    "btn_8": "8",
    "btn_9": "9",
    "btn_10": "10",
    "btn_11": "11",
}


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

    # Создаем объекты бота и диспетчера
    bot = Bot(
        token=config.tg_bot.token,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML),
    )
    dp = Dispatcher()

    # Регистриуем роутеры
    logger.info("Подключаем роутеры")
    # ...

    # Регистрируем миддлвари
    logger.info("Подключаем миддлвари")

    # Этот хэндлер будет срабатывать на команду "/start"
    # и отправлять в чат клавиатуру
    @dp.message(CommandStart())
    async def process_start_command(message: Message):
        # keyboard = create_inline_kb(2, "but_1", "but_3", "but_7")

        # keyboard = create_inline_kb(
        #     2,
        #     btn_tel="Телефон",
        #     btn_email="email",
        #     btn_website="Web-сайт",
        #     btn_vk="VK",
        #     btn_tgbot="Наш телеграм-бот",
        # )

        # keyboard = create_inline_kb(4, last_btn="asdasa", **BUTTONS)

        # keyboard = create_inline_kb(
        #     3, "but_1", "but_2", "but_3", "but_4", "but_5", last_btn="Последняя кнопка"
        # )

        # keyboard = create_inline_kb(
        #     2, last_btn="Последняя кнопка", b_1="1", b_2="2", b_3="3", b_4="4", b_5="5"
        # )

        # keyboard = create_inline_kb(2, last_btn="Последняя кнопка", *BUTTONS)

        keyboard = create_inline_kb(
            2,
            last_btn=None,
            b_1="1",
            b_2="2",
            b_3="3",
            b_4="4",
            b_5="5",
            b_6="Последняя кнопка",
        )

        await message.answer(
            text="Это инлайн-клавиатура, сформированная функцией "
            "<code>create_inline_kb</code>",
            reply_markup=keyboard,
        )

    # Пропускаем накопившиеся апдейты и запускаем polling
    await bot.delete_webhook(drop_pending_updates=True)

    await dp.start_polling(bot)


asyncio.run(main())
