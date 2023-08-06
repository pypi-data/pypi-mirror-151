import unittest
from unittest.mock import MagicMock

from wordleparse.message import Message
from wordleparse.print import print_result


class PrintMessagesTest(unittest.TestCase):
    """
    This TestCase tests whether parsed messages are actually printed to the
    user as well.
    """

    def test_valid_printer(self):
        messages = [Message("23/01/2022, 12:20", "C", "Woordle", "218", "3/6")]

        fn = MagicMock()
        print_result("Woordle", messages, fn)

        fn.assert_any_call("Showing stats for Woordle")
        fn.assert_any_call(build_average_default("C", 1, 0, 3.0))
        fn.assert_any_call("=====================\n")
        self.assertEqual(fn.call_count, 3)

    def test_no_valid_printer(self):
        messages = [Message("23/01/2022, 12:20", "C", "Unknown", "218", "3/6")]

        with self.assertRaises(ValueError) as cm:
            print_result("Unknown", messages)

        self.assertEqual(
            cm.exception.args[0], "No valid printer found for game Unknown."
        )

    def test_multiple_people(self):
        messages = [
            Message("23/01/2022, 12:20", "C", "Woordle", "218", "3/6"),
            Message("23/01/2022, 13:17", "D", "Woordle", "218", "6/6"),
        ]

        fn = MagicMock()
        print_result("Woordle", messages, fn)

        fn.assert_any_call("Showing stats for Woordle")
        fn.assert_any_call(build_average_default("C", 1, 0, 3.0))
        fn.assert_any_call(build_average_default("D", 1, 0, 6.0))
        self.assertEqual(fn.call_count, 4)

    def test_average_score(self):
        messages = [
            Message("23/01/2022, 12:20", "C", "Woordle", "218", "3/6"),
            Message("24/01/2022, 11:28", "C", "Woordle", "219", "3/6"),
            Message("25/01/2022, 00:36", "C", "Woordle", "220", "2/6"),
        ]

        fn = MagicMock()
        print_result("Woordle", messages, fn)

        fn.assert_any_call("Showing stats for Woordle")
        fn.assert_any_call(build_average_default("C", 3, 0, 8 / 3))
        self.assertEqual(fn.call_count, 3)

    def test_failed_attempts(self):
        messages = [
            Message("23/01/2022, 12:20", "C", "Woordle", "218", "3/6"),
            Message("24/01/2022, 11:28", "C", "Woordle", "219", "3/6"),
            Message("25/01/2022, 00:36", "C", "Woordle", "220", "2/6"),
            Message("31/01/2022, 10:55", "C", "Woordle", "226", "X/6"),
        ]
        fn = MagicMock()
        print_result("Woordle", messages, fn)

        fn.assert_any_call("Showing stats for Woordle")
        fn.assert_any_call(build_average_default("C", 4, 1, 8 / 3))
        self.assertEqual(fn.call_count, 3)


class DifferentGamesTest(unittest.TestCase):

    games = [
        "Wordle",
        "Woordle",
        "Woordle6",
        "Worldle",
        "Primel",
        "Letterle",
        "Not Wordle",
        "Vardle",
        "Nerdle",
        "Waffle",
        "Heardle",
        "Hoordle",
    ]

    def test_game(self):
        for game in self.games:
            with self.subTest(game=game):
                messages = [Message("23/01/2022, 13:16", "D", game, "218", "6/6")]
                fn = MagicMock()
                print_result(game, messages, fn)

                fn.assert_any_call(f"Showing stats for {game}")
                fn.assert_any_call(build_average_default("D", 1, 0, 6))
                self.assertEqual(fn.call_count, 3)

    def test_crosswordle(self):
        messages = [Message("05/03/2022, 20:48", "A", "Crosswordle", "45", "11m 41s")]
        fn = MagicMock()
        print_result("Crosswordle", messages, fn)

        fn.assert_any_call("Showing stats for Crosswordle")
        fn.assert_any_call("A: 1 games, average time of 701s")
        self.assertEqual(fn.call_count, 3)

    def test_squardle(self):
        messages = [Message("24/03/2022, 10:13", "A", "Squardle", "49", "2")]
        fn = MagicMock()
        print_result("Squardle", messages, fn)

        fn.assert_any_call("Showing stats for Squardle")
        fn.assert_any_call(
            "A: 1 games, 0 failed attempts (0.0%). "
            + "Average guesses left: 2.0 for the completed games."
        )
        self.assertEqual(fn.call_count, 3)

    def test_diffle(self):
        messages = [
            Message(
                "18/02/2022, 11:11", "C", "Diffle", "2022-2-18", "4 words / 32 letters"
            )
        ]
        fn = MagicMock()
        print_result("Diffle", messages, fn)

        fn.assert_any_call("Showing stats for Diffle")
        fn.assert_any_call(
            "C: 1 games. Average words/letters left: 4.0/32.0 for the completed games."
        )
        self.assertEqual(fn.call_count, 3)


def build_average_default(person, games, failed, score):
    return (
        f"{person}: {games} games, {failed} failed attempts ({failed / games if failed > 0 else 0.0:.1%}). "
        + f"Average score: {score:.2f} for the completed games."
    )
