import unittest

from wordleparse.parsers import woordle6_parser
from wordleparse.message import Message


class Woordle6Test(unittest.TestCase):
    def test_basic_woordle6(self):
        message = """23/01/2022, 12:24 - C: Woordle6 14 5/6

⬛⬛⬛🟨⬛⬛
⬛⬛🟩⬛🟩⬛
⬛🟩🟩⬛🟩🟩
⬛🟩🟩⬛🟩🟩
🟩🟩🟩🟩🟩🟩"""

        result: Message = woordle6_parser.parse(message)
        self.assertEqual(result.game, "Woordle6")
        self.assertEqual(result.date, "23/01/2022, 12:24")
        self.assertEqual(result.person, "C")
        self.assertEqual(result.number, "14")
        self.assertEqual(result.score, "5/6")

    def test_woordle6_failure(self):
        message = """07/02/2022, 09:24 - B: Woordle6 29 X/6

⬛⬛🟨🟨🟩🟩
⬛🟩🟩⬛🟩🟩
⬛🟩🟩⬛🟩🟩
⬛🟩🟩⬛🟩🟩
🟩⬛⬛⬛⬛⬛
🟩🟩🟩⬛🟩🟩"""

        result: Message = woordle6_parser.parse(message)
        self.assertEqual(result.game, "Woordle6")
        self.assertEqual(result.person, "B")
        self.assertEqual(result.score, "X/6")
