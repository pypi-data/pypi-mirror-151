import unittest

from wordleparse.parsers import heardle_parser
from wordleparse.message import Message


class HeardleTest(unittest.TestCase):
    def test_basic_heardle(self):
        message = """22/03/2022, 23:37 - B: #Heardle #25

🔈⬛⬛🟥🟥⬛🟩

https://heardle.app"""

        result: Message = heardle_parser.parse(message)
        self.assertEqual(result.game, "Heardle")
        self.assertEqual(result.date, "22/03/2022, 23:37")
        self.assertEqual(result.person, "B")
        self.assertEqual(result.number, "25")
        self.assertEqual(result.score, "6/6")

    def test_heardle_failure(self):
        message = """25/03/2022, 10:03 - C: #Heardle #28

🔇⬛️⬛️⬛️⬛️⬛️🟥

https://heardle.app"""

        result: Message = heardle_parser.parse(message)
        self.assertEqual(result.person, "C")
        self.assertEqual(result.score, "X/6")

    def test_heardle_other_emojis(self):
        """
        Some of the emoticons used by Heardle use multiple code points.
        In this case calculating the score is less trivial, so hence this test.
        """
        message = """27/03/2022, 13:24 - D: #Heardle #30

🔈⬛️⬛️⬛️⬛️🟩⬜️

https://heardle.app"""

        result: Message = heardle_parser.parse(message)
        self.assertEqual(result.score, "5/6")
