import unittest

from wordleparse.parsers import hoordle_parser
from wordleparse.message import Message


class HoordleTest(unittest.TestCase):
    def test_basic_hoordle(self):
        message = """28/03/2022, 12:09 - B: #Hoordle #15
⬛⬛🟩⬜⬜⬜
https://hoordle.nl"""

        result: Message = hoordle_parser.parse(message)
        self.assertEqual(result.game, "Hoordle")
        self.assertEqual(result.date, "28/03/2022, 12:09")
        self.assertEqual(result.person, "B")
        self.assertEqual(result.number, "15")
        self.assertEqual(result.score, "3/6")

    def test_hoordle_failure(self):
        message = """22/03/2022, 21:08 - C: #Hoordle #9
⬛⬛⬛⬛⬛🟥
https://hoordle.nl"""

        result: Message = hoordle_parser.parse(message)
        self.assertEqual(result.person, "C")
        self.assertEqual(result.score, "X/6")
