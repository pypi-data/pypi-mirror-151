# pylint: disable=no-self-use

import unittest
from unittest.mock import MagicMock

from wordleparse.message import Message
from wordleparse.printers.printers import default_print as sut


class DefaultPrintTest(unittest.TestCase):
    def test_single_message(self):
        messages = [Message("22/03/2022, 17:51", "A", "Wordle", "276", "3/6")]
        fn = MagicMock()

        sut(messages, 1, fn)

        expected = (
            "A: 1 games, 0 failed attempts (0.0%). "
            + "Average score: 3.00 for the completed games."
        )
        fn.assert_called_once_with(expected)

    def test_multiple_messages(self):
        messages = [
            Message("17/03/2022, 13:13", "A", "Wordle", "271", "6/6"),
            Message("18/03/2022, 10:55", "A", "Wordle", "272", "4/6"),
            Message("19/03/2022, 13:36", "A", "Wordle", "273", "4/6"),
            Message("20/03/2022, 15:00", "A", "Wordle", "274", "6/6"),
            Message("21/03/2022, 09:42", "A", "Wordle", "275", "4/6"),
            Message("22/03/2022, 17:51", "A", "Wordle", "276", "3/6"),
        ]
        fn = MagicMock()

        sut(messages, 1, fn)

        expected = (
            f"A: {len(messages)} games, 0 failed attempts (0.0%). "
            + "Average score: 4.50 for the completed games."
        )
        fn.assert_called_once_with(expected)

    def test_with_fail(self):
        messages = [
            Message("16/03/2022, 09:36", "A", "Wordle", "270", "X/6"),
            Message("17/03/2022, 13:13", "A", "Wordle", "271", "6/6"),
            Message("18/03/2022, 10:55", "A", "Wordle", "272", "4/6"),
            Message("19/03/2022, 13:36", "A", "Wordle", "273", "4/6"),
        ]
        fn = MagicMock()

        sut(messages, 1, fn)

        expected = (
            f"A: {len(messages)} games, 1 failed attempts (25.0%). "
            + "Average score: 4.67 for the completed games."
        )
        fn.assert_called_once_with(expected)

    def test_justify(self):
        messages = [Message("22/03/2022, 17:51", "A", "Wordle", "276", "3/6")]
        fn = MagicMock()

        sut(messages, 6, fn)

        expected = (
            "A     : 1 games, 0 failed attempts (0.0%). "
            + "Average score: 3.00 for the completed games."
        )
        fn.assert_called_once_with(expected)

    def test_no_success(self):
        messages = [
            Message("16/03/2022, 09:36", "A", "Wordle", "270", "X/6"),
        ]
        fn = MagicMock()

        sut(messages, 1, fn)

        expected = (
            "A: 1 games, 1 failed attempts (100.0%). "
            + "No average score for the completed games."
        )
        fn.assert_called_once_with(expected)

    def test_other_score(self):
        messages = [
            Message("11/02/2022, 10:22", "B", "Vardle", "14", "6/8"),
        ]
        fn = MagicMock()

        sut(messages, 1, fn)

        expected = (
            "B: 1 games, 0 failed attempts (0.0%). "
            + "Average score: 6.00 for the completed games."
        )
        fn.assert_called_once_with(expected)

    def test_multiple_persons(self):
        messages = [
            Message("16/03/2022, 09:36", "A", "Wordle", "270", "X/6"),
            Message("11/02/2022, 10:22", "B", "Vardle", "14", "6/8"),
        ]

        with self.assertRaises(ValueError) as cm:
            sut(messages, 1)

        self.assertEqual(
            cm.exception.args[0], "Should only print messages of one person"
        )
