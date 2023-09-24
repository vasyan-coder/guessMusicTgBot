import asyncio
import aiofiles
from aiogram import Bot, Dispatcher, Router, types
from aiogram.types import Message, FSInputFile
from aiogram.filters import CommandStart

from os import getenv
import dotenv

import random
from pydub import AudioSegment

dotenv.load_dotenv()

TOKEN = getenv("BOT_TOKEN")

dp = Dispatcher()
bot = Bot(TOKEN)

@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    """
    This handler receives messages with `/start` command
    """
    # song = FSInputFile("music/01_Imagine Dragons - Radioactive_Случайный трек.ogg")
    # await bot.send_chat_action(message.from_user.id, "upload_voice")
    # await bot.send_voice(message.from_user.id, song)


    # with open(f"", 'rb') as audio_file:
    #     await bot.send_audio(message.chat.id, audio=InputFile(audio_file))

    await message.answer(f"Hello!")


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
