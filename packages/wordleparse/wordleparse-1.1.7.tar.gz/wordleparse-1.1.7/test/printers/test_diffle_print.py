# pylint: disable=no-self-use

import unittest
from unittest.mock import MagicMock

from wordleparse.parser import Message
from wordleparse.printers.diffle_printer import print_fn as sut


class DifflePrintTest(unittest.TestCase):
    def test_basic_diffle(self):
        messages = [
            Message(
                "18/02/2022, 11:11", "C", "Diffle", "2022-2-18", "4 words / 32 letters"
            ),
        ]
        fn = MagicMock()

        sut(messages, 1, fn)

        expected = (
            "C: 1 games. Average words/letters left: "
            + "4.0/32.0 for the completed games."
        )
        fn.assert_called_once_with(expected)

    def test_average_diffle(self):
        messages = [
            Message(
                "20/02/2022, 13:23", "A", "Diffle", "2022-2-20", "10 words / 56 letters"
            ),
            Message(
                "21/02/2022, 11:52", "A", "Diffle", "2022-2-21", "5 words / 37 letters"
            ),
        ]
        fn = MagicMock()

        sut(messages, 1, fn)

        expected = (
            "A: 2 games. Average words/letters left: "
            + "7.5/46.5 for the completed games."
        )
        fn.assert_called_once_with(expected)
