import asyncio
import logging

from aiogram import Bot, Dispatcher, F
from aiogram.filters import CommandStart, Command
from config_data.config import Config, load_config
from aiogram.types import (
    KeyboardButton,
    Message,
    ReplyKeyboardMarkup,
    ReplyKeyboardRemove,
    KeyboardButtonPollType,
)
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from aiogram.types.web_app_info import WebAppInfo

# Инициализируем логгер
logger = logging.getLogger(__name__)

dp = Dispatcher()


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

    # Инициализируем бот и диспетчер
    bot = Bot(token=config.tg_bot.token)

    # Создаем объекты кнопок
    # kb_builder = ReplyKeyboardBuilder()
    # button_1 = KeyboardButton(text="Собак 🦮")
    # button_2 = KeyboardButton(text="Огурцов 🥒")

    # buttons: list[KeyboardButton] = [
    #     KeyboardButton(text=f"Кнопка {i + 1}") for i in range(10)
    # ]

    # kb_builder.row(*buttons, width=4)
    # kb_builder.add(*buttons)

    # kb_builder.row(*buttons)

    # В первом ряду 1 кнопка, в последующих 3 кнопки
    # kb_builder.adjust(1, 3)

    # Создаем объект клавиатуры, добавляя в него кнопки
    # keyboard = ReplyKeyboardMarkup(
    #     keyboard=[[button_1, button_2]], resize_keyboard=True, one_time_keyboard=True
    # )

    # Инициализируем билдер
    # kb_builder = ReplyKeyboardBuilder()

    # # Создаем кнопки
    # contact_btn = KeyboardButton(text="Отправить телефон", request_contact=True)
    # geo_btn = KeyboardButton(text="Отправить геолокацию", request_location=True)
    # poll_btn = KeyboardButton(
    #     text="Создать опрос/викторину", request_poll=KeyboardButtonPollType()
    # )

    # # Добавляем кнопки в билдер
    # kb_builder.row(contact_btn, geo_btn, poll_btn, width=1)

    # # Создаем объект клавиатуры
    # keyboard: ReplyKeyboardMarkup = kb_builder.as_markup(
    #     resize_keyboard=True, one_time_keyboard=True
    # )

    # Создаем список списков с кнопками
    keyboard: list[list[KeyboardButton]] = [
        [KeyboardButton(text=str(i)) for i in range(1, 4)],
        [KeyboardButton(text=str(i)) for i in range(4, 7)],
        [KeyboardButton(text=str(i)) for i in range(7, 9)],
    ]

    # Создаем объект клавиатуры, добавляя в него кнопки
    my_keyboard = ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)

    # Этот хэндлер будет срабатывать на команду "/start"
    @dp.message(CommandStart())
    async def process_start_command(message: Message):
        await message.answer(
            text="Экспериментируем со специальными кнопками", reply_markup=my_keyboard
        )

    # Создаем кнопку
    # web_app_btn = KeyboardButton(
    #     text="Start Web App", web_app=WebAppInfo(url="https://stepik.org/")
    # )
    # # Создаем объект клавиатуры
    # web_app_keyboard = ReplyKeyboardMarkup(
    #     keyboard=[[web_app_btn]], resize_keyboard=True
    # )

    # # Этот хэндлер будет срабатывать на команду "/web_app"
    # @dp.message(Command(commands="web_app"))
    # async def process_web_app_command(message: Message):
    #     await message.answer(
    #         text="Экспериментируем со специальными кнопками",
    #         reply_markup=web_app_keyboard,
    #     )

    # Этот хэндлер будет срабатывать на команду "/start"
    # и отправлять в чат клавиатуру
    # @dp.message(CommandStart())
    # async def process_start_command(message: Message):
    #     # await message.answer(text="Чего кошки боятся больше?", reply_markup=keyboard)

    #     await message.answer(
    #         text="Вот такая получается клавиатура",
    #         reply_markup=kb_builder.as_markup(resize_keyboard=True),
    #     )

    # # Этот хэндлер будет срабатывать на ответ "Собак 🦮" и удалять клавиатуру
    # @dp.message(F.text == "Собак 🦮")
    # async def process_dog_answer(message: Message):
    #     await message.answer(
    #         text="Да, несомненно, кошки боятся собак. "
    #         "Но вы видели как они боятся огурцов?",
    #         reply_markup=ReplyKeyboardRemove(),
    #     )

    # # Этот хэндлер будет срабатывать на ответ "Огурцов 🥒" и удалять клавиатуру
    # @dp.message(F.text == "Огурцов 🥒")
    # async def process_cucumber_answer(message: Message):
    #     await message.answer(
    #         text="Да, иногда кажется, что огурцов " "кошки боятся больше",
    #         reply_markup=ReplyKeyboardRemove(),
    #     )

    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
