import unittest

from wordleparse.parsers import worldle_parser
from wordleparse.message import Message


class WorldleTest(unittest.TestCase):
    def test_early_worldle(self):
        """
        Early Worldle games didn't show the "(X%)" at the end of the result.
        """
        message = """17/02/2022, 12:04 - B: #Worldle #27 1/6
🟩🟩🟩🟩🟩
https://worldle.teuteuf.fr"""

        result: Message = worldle_parser.parse(message)
        self.assertEqual(result.game, "Worldle")
        self.assertEqual(result.date, "17/02/2022, 12:04")
        self.assertEqual(result.person, "B")
        self.assertEqual(result.number, "#27")
        self.assertEqual(result.score, "1/6")

    def test_worldle_failure(self):
        message = """20/02/2022, 12:36 - B: #Worldle #30 X/6 (98%) 🙁
🟩🟩🟩🟩⬛⬅️
🟩🟩🟩🟩🟨↖️
🟩🟩🟩🟩🟨⬆️
🟩🟩🟩🟩🟨↗️
🟩🟩🟩🟩⬛↖️
🟩🟩🟩🟩🟨↖️
https://worldle.teuteuf.fr"""

        result: Message = worldle_parser.parse(message)
        self.assertEqual(result.game, "Worldle")
        self.assertEqual(result.score, "X/6 (98%)")

    def test_worldle_hardmode(self):
        message = """17/02/2022, 11:51 - A: #Worldle #27 3/6 🙈
🟩⬛⬛⬛⬛
🟩🟩🟩🟨⬛
🟩🟩🟩🟩🟩
https://worldle.teuteuf.fr"""

        result = worldle_parser.parse(message)
        self.assertEqual(result.game, "Worldle")
        self.assertEqual(result.date, "17/02/2022, 11:51")
        self.assertEqual(result.person, "A")
        self.assertEqual(result.number, "#27")
        self.assertEqual(result.score, "3/6 🙈")
