import unittest

from wordleparse.parsers import crosswordle_parser
from wordleparse.message import Message


class CrosswordleTest(unittest.TestCase):
    def test_basic_crosswordle(self):
        # pylint: disable=line-too-long
        message = """05/03/2022, 20:48 - C: Daily Crosswordle 45: 11m 41s https://crosswordle.vercel.app/?daily=1

⬜⬜⬜⬜⬜
⬜⬜⬜⬜⬜
⬜🟨⬜🟨⬜
⬜🟨⬜🟨🟩
🟩⬜🟩⬜🟩
🟩🟩🟩🟩🟩"""

        result: Message = crosswordle_parser.parse(message)
        self.assertEqual(result.game, "Crosswordle")
        self.assertEqual(result.date, "05/03/2022, 20:48")
        self.assertEqual(result.person, "C")
        self.assertEqual(result.number, "45")
        self.assertEqual(result.score, "11m 41s")

    def test_crosswordle_singledigit_score(self):
        # pylint: disable=line-too-long
        message = """11/03/2022, 09:40 - C: Daily Crosswordle 51: 3m 3s https://crosswordle.vercel.app/?daily=1

⬛⬛🟨⬛⬛
⬛🟨🟨⬛⬛
🟨🟨⬛⬛🟩
🟩🟩🟩🟩🟩"""

        result: Message = crosswordle_parser.parse(message)
        self.assertEqual(result.score, "3m 3s")

    def test_crosswordle_within_one_minute(self):
        # pylint: disable=line-too-long
        message = """21/03/2022, 11:18 - C: Daily Crosswordle 61: 54s https://crosswordle.vercel.app/?daily=1

⬛⬛🟨⬛⬛
⬛⬛⬛🟨🟨
🟨🟩⬛⬛🟩
🟩🟩🟩🟩🟩"""

        result = crosswordle_parser.parse(message)
        self.assertEqual(result.score, "54s")

    def test_crosswordle_zero_seconds(self):
        # pylint: disable=line-too-long
        message = """22/03/2022, 09:24 - C: Daily Crosswordle 62: 1m 0s https://crosswordle.vercel.app/?daily=1

⬛⬛🟨⬛⬛
⬛🟨⬛🟨⬛
⬛🟩🟨🟩⬛
🟩🟩🟩🟩🟩"""

        result = crosswordle_parser.parse(message)
        self.assertEqual(result.score, "1m 0s")
