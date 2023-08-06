import logging
from collections.abc import Iterator

from wordleparse.message import Message
from wordleparse.parser import MessageParser
from wordleparse.parsers import (
    wordle_parser,
    woordle_parser,
    woordle6_parser,
    worldle_parser,
    squardle_win_parser,
    squardle_loss_parser,
    crosswordle_parser,
    primel_parser,
    letterle_parser,
    not_wordle_parser,
    nerdle_parser,
    vardle_parser,
    waffle_parser,
    heardle_parser,
    hoordle_parser,
    diffle_parser,
)
from wordleparse.util import group
from wordleparse.errors import UnparsableError

parsers: list[MessageParser] = [
    wordle_parser,
    woordle_parser,
    woordle6_parser,
    worldle_parser,
    squardle_win_parser,
    squardle_loss_parser,
    crosswordle_parser,
    primel_parser,
    letterle_parser,
    not_wordle_parser,
    nerdle_parser,
    vardle_parser,
    waffle_parser,
    heardle_parser,
    hoordle_parser,
    diffle_parser,
]


def parse_messages(lines: list[str]) -> Iterator[Message]:
    grouped_messages = group(iter(lines))

    for message_lines in grouped_messages:
        message = "".join(message_lines)
        try:
            yield parse_message(message)
        except UnparsableError:
            continue


def parse_message(message: str) -> Message:
    """
    Method that takes a message from a chat and returns a Message object.
    Throws UnparsableError if the message can't be parsed by any of the known
    parsers.
    """
    for parser in parsers:
        if parser.can_parse(message):
            return parser.parse(message)

    logging.info("Couldn't parse %s", message[:-1])
    raise UnparsableError()
