import asyncio
import random
from os import getenv, listdir

import dotenv
from aiogram import Bot, Dispatcher
from aiogram.filters import CommandStart
from aiogram.types import Message, FSInputFile
from pydub import AudioSegment

dotenv.load_dotenv()

TOKEN = getenv("BOT_TOKEN")

dp = Dispatcher()
bot = Bot(TOKEN)

users = {}


@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    """
    This handler receives messages with `/start` command
    """
    files = listdir("music")
    random_song_number = random.randint(0, len(files) - 1)
    song_name = files[random_song_number]

    # save user in db
    users[message.chat.id] = random_song_number

    song = FSInputFile(f"music/{song_name}")
    await bot.send_chat_action(message.from_user.id, "upload_voice")
    await bot.send_voice(message.from_user.id, song)
    await bot.send_message(message.from_user.id, "Напишите название исполнителя данной песни")


@dp.message()
async def guess_song_handler(message: Message) -> None:
    """
    This handler check user answer
    """
    files = listdir("music")
    chat_id = message.chat.id

    if chat_id in users:
        if message.text == files[users[chat_id]].split("-")[0].strip():
            await bot.send_message(chat_id,
                                   f"Угадали. Это была песня: {files[users[chat_id]][:-4]}.\nПропишите /start для начала новой игры")
        else:
            await bot.send_message(chat_id,
                                   f"Не угадали. Это была песня: {files[users[chat_id]][:-4]}.\nПропишите /start для начала новой игры")
    else:
        await bot.send_message(chat_id, "Пропишите /start для начала игры")


def extract_random_segment(input_file):
    audio = AudioSegment.from_file(input_file, format="ogg")
    audio_duration = len(audio)
    start_time = random.randint(0, audio_duration - 5000)
    segment = audio[start_time:start_time + 5000]
    return segment


async def main() -> None:
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
