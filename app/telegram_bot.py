import asyncio
import logging
import sys
from os import getenv

from aiogram import Bot, Dispatcher, Router, types
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import Message
from aiogram.utils.markdown import hbold
import dotenv

dotenv.load_dotenv()
TOKEN = getenv("BOT_TOKEN")
users = []
dp = Dispatcher()
bot = Bot(TOKEN, parse_mode=ParseMode.HTML)


@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    with open(file='users.txt', mode='a', encoding='utf-8') as file:
        file.write(str(message.chat.id))

    await message.answer(
        f"Привет, {hbold(message.from_user.full_name)}! Зарегистрировал тебя для получения обновлений!")


@dp.message()
async def echo_handler(message: types.Message) -> None:
    await message.answer('Ты уже зарегистрирован! Когда будут новые сообщения - обещаю, сообщу тебе первым.')


async def send_message(message: str) -> None:
    sended = []
    for user in users:
        try:
            if user not in sended:
                await bot.send_message(user, message)
                sended.append(user)
        except:
            pass


async def main() -> None:
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
