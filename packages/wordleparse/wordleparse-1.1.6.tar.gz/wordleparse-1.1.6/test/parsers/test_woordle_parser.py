import unittest

from wordleparse.parsers import woordle_parser
from wordleparse.message import Message


class WoordleTest(unittest.TestCase):
    def test_basic_woordle(self):
        message = """23/01/2022, 12:20 - C: Woordle 218 3/6

⬛⬛🟨🟨🟨
🟩🟨🟨⬛🟨
🟩🟩🟩🟩🟩"""

        result: Message = woordle_parser.parse(message)
        self.assertEqual(result.game, "Woordle")
        self.assertEqual(result.date, "23/01/2022, 12:20")
        self.assertEqual(result.person, "C")
        self.assertEqual(result.number, "218")
        self.assertEqual(result.score, "3/6")

    def test_woordle_failure(self):
        message = """27/01/2022, 00:08 - D: Woordle 222 X/6

⬛🟩⬛🟨⬛
⬛🟩⬛⬛🟩
⬛🟩⬛⬛🟩
⬛🟩⬛⬛🟩
⬛🟩⬛⬛🟩
⬛🟩⬛🟩🟩"""

        result: Message = woordle_parser.parse(message)
        self.assertEqual(result.person, "D")
        self.assertEqual(result.score, "X/6")
