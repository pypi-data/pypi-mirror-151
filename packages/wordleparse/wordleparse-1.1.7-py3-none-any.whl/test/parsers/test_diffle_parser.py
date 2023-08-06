import unittest

from wordleparse.parsers import diffle_parser
from wordleparse.message import Message


class DiffleTest(unittest.TestCase):
    def test_basic_diffle(self):
        message = """18/02/2022, 11:11 - C: Diffle 2022-2-18
4 words / 32 letters

⚪🟢⚪🟡🟢⚪⚪⚪⚪
⚪🟢🟢🟢🟡⚪⚪🟡⚪
🟢🟢🟢🟢⚪
🟩🟩🟩🟩🟩🟩🟩🟩🟩

https://hedalu244.github.io/diffle/"""

        result: Message = diffle_parser.parse(message)
        self.assertEqual(result.game, "Diffle")
        self.assertEqual(result.date, "18/02/2022, 11:11")
        self.assertEqual(result.person, "C")
        self.assertEqual(result.number, "2022-2-18")
        self.assertEqual(result.score, "4 words / 32 letters")

    def test_diffle_more_words(self):
        # We occasionally omit the final line in Diffle since that spoils the
        # resulting word length. The code should handle that as well
        message = """20/02/2022, 13:23 - A: Diffle 2022-2-20
10 words / 56 letters

⚪🟢⚪⚪⚪🟢⚪⚪🟡⚪
⚪⚪🟢⚪🟢🟡
⚪🟢🟢⚪🟡
🟢⚪🟢🟢⚪
🟢🟢🟡
⚪🟢🟢🟢🟡
🟢🟢⚪⚪🟡
🟢🟢🟢🟡⚪
⚪🟢🟢🟢🟢

https://hedalu244.github.io/diffle/"""

        result: Message = diffle_parser.parse(message)
        self.assertEqual(result.score, "10 words / 56 letters")

    def test_diffle_singlenumbered_day(self):
        message = """01/03/2022, 12:14 - B: Diffle 2022-3-1
4 words / 24 letters

🟢⚪⚪⚪⚪⚪⚪⚪🟢
⚪🟢🟢⚪🟢
⚪🟢🟢🟢🟢

https://hedalu244.github.io/diffle/"""

        result: Message = diffle_parser.parse(message)
        self.assertEqual(result.number, "2022-3-1")
