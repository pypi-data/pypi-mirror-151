import unittest

from wordleparse.parsers import waffle_parser
from wordleparse.message import Message


class WaffleTest(unittest.TestCase):
    def test_basic_waffle(self):
        message = """18/05/2022, 09:12 - C: #waffle117 3/5

🟩🟩🟩🟩🟩
🟩⭐🟩⬜🟩
🟩🟩⭐🟩🟩
🟩⬜🟩⭐🟩
🟩🟩🟩🟩🟩

🔥 streak: 42
🥈 #wafflesilverteam
wafflegame.net"""

        result: Message = waffle_parser.parse(message)
        self.assertEqual(result.game, "Waffle")
        self.assertEqual(result.date, "18/05/2022, 09:12")
        self.assertEqual(result.person, "C")
        self.assertEqual(result.number, "117")
        self.assertEqual(result.score, "3/5")

    def test_waffle_fail(self):
        message = """04/04/2022, 01:17 - A: #waffle72 X/5

⬛⬛⬛⬛⬛
⬛⬜⬛⬜⬛
⬛⬛⬛⬛⬛
⬛⬜⬛⬜⬛
⬛⬛⬛⬛⬛

💔 streak: 0
wafflegame.net"""

        result: Message = waffle_parser.parse(message)
        self.assertEqual(result.score, "X/5")

    def test_canuffle(self):
        # Canuffle was a Canadian version of Waffle, played on 29/04
        message = """29/04/2022, 09:45 - C: #canuffle 1/5

🟥🟥🟥🟥🟥
🟥⬜🟥⬜🟥
🟥🟥🍁🟥🟥
🟥⬜🟥⬜🟥
🟥🟥🟥🟥🟥

🔥 streak: 24
🏆 #waffleelite
wafflegame.net"""

        result = waffle_parser.parse(message)
        self.assertEqual(result.game, "Waffle")
        self.assertEqual(result.score, "1/5")

    def test_waffle_zero(self):
        message = """10/05/2022, 11:36 - D: #waffle109 0/5

🟩🟩🟩🟩🟩
🟩⬜🟩⬜🟩
🟩🟩🟩🟩🟩
🟩⬜🟩⬜🟩
🟩🟩🟩🟩🟩

🔥 streak: 8
wafflegame.net"""

        result = waffle_parser.parse(message)
        self.assertEqual(result.score, "0/5")
