import unittest

from wordleparse.parsers import squardle_win_parser, squardle_loss_parser
from wordleparse.message import Message


class SquardleWinTest(unittest.TestCase):
    def test_basic_squardle(self):
        message = """12/03/2022, 11:51 - A: I won Daily Squardle #37 with 2 guesses to spare!
Board after 3 guesses:
🟥🟥⬜🟩🟨
⬜🔳🟩🔳⬜
⬜⬜🟩🟨🟥
⬜🔳🟩🔳⬜
⬜🟩⬜⬜⬛
https://fubargames.se/squardle/"""

        result: Message = squardle_win_parser.parse(message)
        self.assertEqual(result.game, "Squardle")
        self.assertEqual(result.date, "12/03/2022, 11:51")
        self.assertEqual(result.person, "A")
        self.assertEqual(result.number, "#37")
        self.assertEqual(result.score, "2")

    def test_squardle_one_guess_left(self):
        message = """26/03/2022, 11:24 - A: I won Daily Squardle #51 with 1 guess to spare!
Board after 3 guesses:
⬛⬜⬜🟥🟥
🟥🔳⬜🔳🟧
🟩🟨⬜⬜🟨
⬜🔳⬜🔳🟩
🟧🟨🟨⬜🟥
https://fubargames.se/squardle/"""

        result: Message = squardle_win_parser.parse(message)
        self.assertEqual(result.score, "1")


class SquardleLossTest(unittest.TestCase):
    def test_squardle_loss(self):
        message = """25/03/2022, 17:02 - B: I solved 19/21 squares in Daily Squardle #50
🟩🟩🟩🟩🟩
🟩🔳🟩🔳⬜
🟩🟩🟩🟩🟩
🟩🔳🟩🔳🟥
🟩🟩🟩🟩🟩
https://fubargames.se/squardle/"""

        result: Message = squardle_loss_parser.parse(message)
        self.assertEqual(result.game, "Squardle")
        self.assertEqual(result.date, "25/03/2022, 17:02")
        self.assertEqual(result.person, "B")
        self.assertEqual(result.number, "#50")
        self.assertEqual(result.score, "19/21")
