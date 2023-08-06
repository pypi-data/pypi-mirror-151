# pylint: disable=no-self-use

import unittest
from unittest.mock import MagicMock

from wordleparse.parser import Message
from wordleparse.printers.squardle_printer import print_fn as sut


class SquardlePrintTest(unittest.TestCase):
    def test_basic_squardle(self):
        messages = [
            Message("24/03/2022, 10:13", "A", "Squardle", "49", "2"),
            Message("25/03/2022, 10:40", "A", "Squardle", "50", "3"),
        ]
        fn = MagicMock()

        sut(messages, 1, fn)

        expected = (
            "A: 2 games, 0 failed attempts (0.0%). Average guesses left: "
            + "2.5 for the completed games."
        )
        fn.assert_called_once_with(expected)

    def test_squardle_with_fail(self):
        messages = [
            Message("21/03/2022, 09:48", "B", "Squardle", "46", "5"),
            Message("25/03/2022, 17:02", "B", "Squardle", "50", "19/21"),
        ]
        fn = MagicMock()

        sut(messages, 1, fn)

        expected = (
            "B: 2 games, 1 failed attempts (50.0%). Average guesses left: "
            + "5.0 for the completed games."
        )
        fn.assert_called_once_with(expected)

    def test_squardle_without_win(self):
        messages = [
            Message("25/03/2022, 17:02", "B", "Squardle", "50", "19/21"),
        ]
        fn = MagicMock()

        sut(messages, 1, fn)

        expected = (
            "B: 1 games, 1 failed attempts (100.0%). "
            + "No average guesses left for the completed games."
        )
