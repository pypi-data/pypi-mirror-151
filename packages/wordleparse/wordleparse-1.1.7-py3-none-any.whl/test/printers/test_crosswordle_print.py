# pylint: disable=no-self-use

import unittest
from unittest.mock import MagicMock

from wordleparse.parser import Message
from wordleparse.printers.crosswordle_printer import print_fn as sut


class CrosswordlePrintTest(unittest.TestCase):
    def test_basic_crosswordle(self):
        messages = [
            Message("05/03/2022, 20:48", "A", "Crosswordle", "45", "11m 41s"),
            Message("06/03/2022, 11:49", "A", "Crosswordle", "46", "4m 28s"),
        ]
        fn = MagicMock()

        sut(messages, 1, fn)

        expected = "A: 2 games, average time of 484s"
        fn.assert_called_once_with(expected)

    def test_crosswordle_with_fast_score(self):
        messages = [
            Message("16/03/2022, 10:48", "A", "Crosswordle", "56", "3m 7s"),
            Message("21/03/2022, 11:18", "A", "Crosswordle", "61", "54s"),
            Message("22/03/2022, 09:24", "A", "Crosswordle", "62", "1m 0s"),
        ]
        fn = MagicMock()

        sut(messages, 1, fn)

        expected = "A: 3 games, average time of 100s"
        fn.assert_called_once_with(expected)
