import unittest

from wordleparse.parsers import vardle_parser
from wordleparse.message import Message


class VardleTest(unittest.TestCase):
    def test_basic_vardle(self):
        message = """01/02/2022, 14:52 - A: Vardle 4 8/8

⚪
⚪
🟡
🟢
🟢
🟢
🟢
🟢

https://vardle.netlify.app/"""

        result: Message = vardle_parser.parse(message)
        self.assertEqual(result.game, "Vardle")
        self.assertEqual(result.date, "01/02/2022, 14:52")
        self.assertEqual(result.person, "A")
        self.assertEqual(result.number, "4")
        self.assertEqual(result.score, "8/8")

    def test_vardle_failure(self):
        message = """01/02/2022, 14:52 - C: Vardle 4 X/8

🟢
🟢
🟢
🟢
🟢
🟢
🟢
🟢

https://vardle.netlify.app/"""

        result: Message = vardle_parser.parse(message)
        self.assertEqual(result.score, "X/8")
