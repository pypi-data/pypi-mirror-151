import unittest

from wordleparse.parsers import nerdle_parser
from wordleparse.message import Message


class NerdleTest(unittest.TestCase):
    def test_old_nerdle(self):
        """
        The old Nerdle was named "Nerdle" and should be parsed correctly.
        """
        message = """01/02/2022, 14:11 - A: Nerdle 13 4/6

⬛⬛🟪⬛🟪🟪🟪⬛
🟪⬛⬛🟩🟪🟪⬛🟩
⬛⬛🟩🟩⬛🟩⬛🟩
🟩🟩🟩🟩🟩🟩🟩🟩

https://nerdlegame.com #nerdle"""

        result: Message = nerdle_parser.parse(message)
        self.assertEqual(result.game, "Nerdle")
        self.assertEqual(result.date, "01/02/2022, 14:11")
        self.assertEqual(result.person, "A")
        self.assertEqual(result.number, "13")
        self.assertEqual(result.score, "4/6")

    def test_nerdlegame(self):
        """
        The new Nerdle is named "nerdlegame" and should be parsed correctly,
        also with the name "Nerdle".
        """
        message = """06/02/2022, 21:51 - A: nerdlegame 18 4/6

🟩⬛⬛⬛⬛🟪⬛🟪
🟩🟪⬛🟪🟪🟪⬛🟩
🟩⬛⬛🟩⬛⬛🟩🟩
🟩🟩🟩🟩🟩🟩🟩🟩

https://nerdlegame.com #nerdle"""

        result: Message = nerdle_parser.parse(message)
        self.assertEqual(result.game, "Nerdle")
        self.assertEqual(result.score, "4/6")
