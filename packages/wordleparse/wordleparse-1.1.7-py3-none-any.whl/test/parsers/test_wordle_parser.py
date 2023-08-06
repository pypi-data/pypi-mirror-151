import unittest

from wordleparse.parsers import wordle_parser
from wordleparse.message import Message


class WordleTest(unittest.TestCase):
    def test_basic_wordle(self):
        message = """23/01/2022, 13:16 - D: Wordle 218 3/6

⬛⬛⬛⬛⬛
🟨🟩🟩🟨⬛
🟩🟩🟩🟩🟩"""

        result: Message = wordle_parser.parse(message)
        self.assertEqual(result.game, "Wordle")
        self.assertEqual(result.date, "23/01/2022, 13:16")
        self.assertEqual(result.person, "D")
        self.assertEqual(result.number, "218")
        self.assertEqual(result.score, "3/6")

    def test_wordle_failure(self):
        message = """21/02/2022, 09:08 - B: Wordle 247 X/6

⬛🟨⬛⬛🟨
⬛🟨🟨🟩⬛
🟨🟨⬛🟩⬛
🟩⬛⬛🟩🟩
🟩⬛⬛🟩🟩
🟩🟩⬛🟩🟩"""

        result: Message = wordle_parser.parse(message)
        self.assertEqual(result.score, "X/6")

    def test_wordle_hardmode(self):
        message = """30/01/2022, 11:58 - C: Wordle 225 5/6*

⬛⬛⬛🟨⬛
⬛⬛⬛⬛🟨
⬛🟩⬛⬛⬛
🟨🟩🟩🟩⬛
🟩🟩🟩🟩🟩"""

        result = wordle_parser.parse(message)
        self.assertEqual(result.score, "5/6*")
