import unittest
from unittest.mock import Mock, patch

from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from bot.main import command_start_handler, guess_song_handler


class MockBotTestCase(unittest.TestCase):

    def setUp(self):
        self.message = Mock(Message)
        self.message.chat = Mock()  # Create a mock for the chat attribute
        self.message.chat.id = 123  # Set the chat id for testing
        self.state = Mock(FSMContext)

    @patch('your_bot.bot', autospec=True)
    @patch('your_bot.listdir', return_value=['song1.ogg', 'song2.ogg'])  # Mock the listdir function
    @patch('random.randint', return_value=0)  # Mock random.randint to always return 0
    async def test_command_start_handler(self, mocked_randint, mocked_listdir, mocked_bot):
        await command_start_handler(self.message, self.state)

        # Assertions
        mocked_listdir.assert_called_once_with("../music")
        mocked_randint.assert_called_once_with(0, 1)  # Since there are 2 files in the list
        mocked_bot.send_chat_action.assert_called_once_with(self.message.from_user.id, "upload_voice")
        mocked_bot.send_voice.assert_called_once()
        mocked_bot.send_message.assert_called_once_with(self.message.from_user.id,
                                                        "Напишите название исполнителя данной песни")

    @patch('your_bot.bot', autospec=True)
    @patch('your_bot.listdir', return_value=['song1.ogg', 'song2.ogg'])  # Mock the listdir function
    async def test_guess_song_handler_correct_answer(self, mocked_listdir, mocked_bot):
        users = {123: 0}
        self.message.chat.id = 123
        self.message.text = "song1"

        await guess_song_handler(self.message, self.state)

        mocked_listdir.assert_called_once_with("../music")
        mocked_bot.send_message.assert_called_once_with(123,
                                                        "Угадали. Это была песня: song1.\nПропишите /start для начала "
                                                        "новой игры")

    @patch('your_bot.bot', autospec=True)
    @patch('your_bot.listdir', return_value=['song1.ogg', 'song2.ogg'])  # Mock the listdir function
    async def test_guess_song_handler_wrong_answer(self, mocked_listdir, mocked_bot):
        users = {123: 0}
        self.message.chat.id = 123
        self.message.text = "wrong_song"

        await guess_song_handler(self.message, self.state)

        # Assertions for a wrong answer
        mocked_listdir.assert_called_once_with("../music")
        mocked_bot.send_message.assert_called_once_with(123,
                                                        "Не угадали. Это была песня: song1.\nПропишите /start для "
                                                        "начала новой игры")

    @patch('your_bot.bot', autospec=True)
    async def test_guess_song_handler_no_game(self, mocked_bot):
        users = {}
        self.message.chat.id = 123
        self.message.text = "song1"

        await guess_song_handler(self.message, self.state)

        mocked_bot.send_message.assert_called_once_with(123, "Пропишите /start для начала игры")

        raise "Not found exception"


if __name__ == '__main__':
    unittest.main()
