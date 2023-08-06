import unittest

from wordleparse.message import Message
from wordleparse.parse import parse_messages


def sut(lines: list[str]) -> list[Message]:
    return list(parse_messages(lines))


class ParseMessagesTest(unittest.TestCase):
    """
    This TestCase tests whether (WhatsApp) messages are parsed correctly. It's
    perhaps more akin to an integration test than a unit test, since the
    parsers themselves have been tested individually, and this mainly tests
    whether everything is 'linked' correctly.
    """

    def test_random_strings_are_not_parsed(self):
        lines = ["Hello, World!", "23-01-2020 random message"]

        messages = sut(lines)

        self.assertEqual(messages, [])

    def test_basic_wordle_message_parsed(self):
        lines = [
            '23/01/2022, 12:20 - You created group "group"',
            """23/01/2022, 12:20 - C: Woordle 218 3/6

⬛⬛🟨🟨🟨
🟩🟨🟨⬛🟨
🟩🟩🟩🟩🟩""",
        ]

        messages = sut(lines)

        expected = [Message("23/01/2022, 12:20", "C", "Woordle", "218", "3/6")]
        self.assertEqual(expected, messages)

    def test_incorrect_date_format_not_parsed(self):
        lines = [
            """23-01-2022, 12:20 - C: Woordle 218 3/6

⬛⬛🟨🟨🟨
🟩🟨🟨⬛🟨
🟩🟩🟩🟩🟩"""
        ]

        messages = sut(lines)

        self.assertEqual(messages, [])

    def test_multiple_people(self):
        lines = [
            """15/02/2022, 09:07 - A: Woordle6 37 2/6

🟨⬛⬛⬛⬛🟨
🟩🟩🟩🟩🟩🟩""",
            """04/03/2022, 09:07 - D: Woordle6 54 2/6

⬜⬜🟩🟩⬜🟨
🟩🟩🟩🟩🟩🟩""",
        ]

        messages = sut(lines)

        expected = [
            Message("15/02/2022, 09:07", "A", "Woordle6", "37", "2/6"),
            Message("04/03/2022, 09:07", "D", "Woordle6", "54", "2/6"),
        ]
        self.assertEqual(messages, expected)

    def test_multiple_games(self):
        lines = [
            """04/03/2022, 09:07 - D: Woordle6 54 2/6

⬜⬜🟩🟩⬜🟨
🟩🟩🟩🟩🟩🟩""",
            """04/03/2022, 09:12 - D: Vardle 35 3/8

⚪
⚪
🟢""",
        ]

        messages = sut(lines)

        expected = [
            Message("04/03/2022, 09:07", "D", "Woordle6", "54", "2/6"),
            Message("04/03/2022, 09:12", "D", "Vardle", "35", "3/8"),
        ]
        self.assertEqual(messages, expected)

    def test_text_appended(self):
        """Appending a text to a game does not make a difference."""
        lines = [
            """28/01/2022, 00:16 - D: Wordle 223 2/6

🟨🟩⬛⬛⬛
🟩🟩🟩🟩🟩
Kobe"""
        ]

        messages = sut(lines)
        self.assertEqual(
            messages, [Message("28/01/2022, 00:16", "D", "Wordle", "223", "2/6")]
        )


class DifferentGamesTest(unittest.TestCase):
    """
    TestCase to test that the different games are all integrated.
    """

    def test_wordle(self):
        lines = [
            """28/01/2022, 00:16 - D: Wordle 223 2/6

        🟨🟩⬛⬛⬛
        🟩🟩🟩🟩🟩"""
        ]

        messages = sut(lines)
        self.assertEqual(
            messages, [Message("28/01/2022, 00:16", "D", "Wordle", "223", "2/6")]
        )

    def test_woordle(self):
        lines = [
            """01/02/2022, 10:48 - C: Woordle 227 1/6

🟩🟩🟩🟩🟩"""
        ]
        messages = sut(lines)
        self.assertEqual(
            messages, [Message("01/02/2022, 10:48", "C", "Woordle", "227", "1/6")]
        )

    def test_woordle6(self):
        lines = [
            """26/01/2022, 00:42 - B: Woordle6 17 2/6

⬛🟨🟩🟨⬛🟨
🟩🟩🟩🟩🟩🟩"""
        ]

        messages = sut(lines)
        self.assertEqual(
            messages, [Message("26/01/2022, 00:42", "B", "Woordle6", "17", "2/6")]
        )

    def test_worldle(self):
        lines = [
            """17/02/2022, 11:51 - A: #Worldle #27 3/6 🙈
🟩⬛⬛⬛⬛
🟩🟩🟩🟨⬛
🟩🟩🟩🟩🟩
https://worldle.teuteuf.fr"""
        ]

        messages = sut(lines)
        self.assertEqual(
            messages, [Message("17/02/2022, 11:51", "A", "Worldle", "#27", "3/6 🙈")]
        )

    def test_squardle_win(self):
        lines = [
            """12/03/2022, 11:51 - A: I won Daily Squardle #37 with 2 guesses to spare!
Board after 3 guesses:
🟥🟥⬜🟩🟨
⬜🔳🟩🔳⬜
⬜⬜🟩🟨🟥
⬜🔳🟩🔳⬜
⬜🟩⬜⬜⬛
https://fubargames.se/squardle/"""
        ]

        messages = sut(lines)
        self.assertEqual(
            messages, [Message("12/03/2022, 11:51", "A", "Squardle", "#37", "2")]
        )

    def test_squardle_loss(self):
        lines = [
            """25/03/2022, 17:02 - B: I solved 19/21 squares in Daily Squardle #50
🟩🟩🟩🟩🟩
🟩🔳🟩🔳⬜
🟩🟩🟩🟩🟩
🟩🔳🟩🔳🟥
🟩🟩🟩🟩🟩
https://fubargames.se/squardle/"""
        ]

        messages = sut(lines)
        self.assertEqual(
            messages, [Message("25/03/2022, 17:02", "B", "Squardle", "#50", "19/21")]
        )

    def test_crosswordle(self):
        lines = [
            # pylint: disable=line-too-long
            """30/03/2022, 09:16 - B: Daily Crosswordle 70: 3m 11s https://crosswordle.vercel.app/?daily=1

🟨⬜⬜⬜⬜
🟨🟨⬜🟨⬜
⬜🟨⬜🟩🟩
🟩🟩🟩🟩🟩"""
        ]

        messages = sut(lines)
        self.assertEqual(
            messages, [Message("30/03/2022, 09:16", "B", "Crosswordle", "70", "3m 11s")]
        )

    def test_primel(self):
        lines = [
            """23/01/2022, 13:59 - A: Primel 22 4/6

⬜🟨⬜🟩🟨
⬜🟨⬜⬜🟨
⬜🟩🟨🟩🟨
🟩🟩🟩🟩🟩"""
        ]

        messages = sut(lines)
        self.assertEqual(
            messages, [Message("23/01/2022, 13:59", "A", "Primel", "22", "4/6")]
        )

    def test_letterle(self):
        lines = [
            """25/01/2022, 12:58 - C: Letterle 1/26
🟩
 https://edjefferson.com/letterle/"""
        ]

        messages = sut(lines)
        self.assertEqual(
            messages, [Message("25/01/2022, 12:58", "C", "Letterle", " ", "1/26")]
        )

    def test_not_wordle(self):
        lines = [
            """26/01/2022, 10:45 - C: Not Wordle 25 3/6

⬜⬜⬜⬜⬜
🟩🟨🟨⬜⬜
🟩🟩🟩🟩🟩"""
        ]

        messages = sut(lines)
        self.assertEqual(
            messages, [Message("26/01/2022, 10:45", "C", "Not Wordle", "25", "3/6")]
        )

    def test_nerdle(self):
        lines = [
            """01/02/2022, 14:11 - A: Nerdle 13 4/6

⬛⬛🟪⬛🟪🟪🟪⬛
🟪⬛⬛🟩🟪🟪⬛🟩
⬛⬛🟩🟩⬛🟩⬛🟩
🟩🟩🟩🟩🟩🟩🟩🟩

https://nerdlegame.com #nerdle"""
        ]

        messages = sut(lines)
        self.assertEqual(
            messages, [Message("01/02/2022, 14:11", "A", "Nerdle", "13", "4/6")]
        )

    def test_vardle(self):
        lines = [
            """20/02/2022, 13:04 - A: Vardle 23 2/8

⚪
🟢

https://vardle.netlify.app/"""
        ]

        messages = sut(lines)
        self.assertEqual(
            messages, [Message("20/02/2022, 13:04", "A", "Vardle", "23", "2/8")]
        )

    def test_waffle(self):
        lines = [
            """03/04/2022, 21:15 - C: #waffle72 4/5

🟩🟩🟩🟩🟩
🟩⭐🟩⭐🟩
🟩🟩🟩🟩🟩
🟩⭐🟩⭐🟩
🟩🟩🟩🟩🟩

🔥 streak: 1
wafflegame.net"""
        ]

        messages = sut(lines)
        self.assertEqual(
            messages, [Message("03/04/2022, 21:15", "C", "Waffle", "72", "4/5")]
        )

    def test_heardle(self):
        lines = [
            """22/03/2022, 21:06 - C: #Heardle #25

🔈⬛⬛🟥🟥🟥🟩

https://heardle.app"""
        ]

        messages = sut(lines)
        self.assertEqual(
            messages, [Message("22/03/2022, 21:06", "C", "Heardle", "25", "6/6")]
        )

    def test_hoordle(self):
        lines = [
            """22/03/2022, 21:08 - C: #Hoordle #9
⬛⬛⬛⬛⬛🟥
https://hoordle.nl"""
        ]

        messages = sut(lines)
        self.assertEqual(
            messages, [Message("22/03/2022, 21:08", "C", "Hoordle", "9", "X/6")]
        )
