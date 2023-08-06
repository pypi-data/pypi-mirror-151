import re

from wordleparse.message import Message
from wordleparse.errors import UnparsableError


BEGIN_RE = r"([0-9]{2}/[0-9]{2}/[0-9]{4}, [0-9]{2}:[0-9]{2}) - ([\s\S]+)"
PERSON_RE = r"([\w <]+): ([\s\S]+)"


class MessageParser:
    def __init__(
        self,
        game,
        game_parser,
    ):
        self.game = game
        self.game_parser = game_parser

    def can_parse(self, message: str) -> bool:
        try:
            self.parse(message)
            return True
        except UnparsableError:
            return False

    def parse(self, message: str) -> Message:
        date, rest = self._parse_begin(message)
        person, rest = self._parse_person(rest)
        number, score = self.game_parser.parse_game(rest)
        return Message(date, person, self.game, number, score)

    @staticmethod
    def _parse_begin(message: str):
        m = re.match(BEGIN_RE, message)
        if not m:
            raise UnparsableError()

        return m.groups()

    @staticmethod
    def _parse_person(message: str):
        m = re.match(PERSON_RE, message)
        if not m:
            raise UnparsableError()

        return m.groups()


class RegexParser:
    def __init__(self, game_regex):
        self.game_regex = game_regex

    def parse_game(self, message: str):
        m = re.match(self.game_regex, message)
        if not m:
            raise UnparsableError()

        return m.group("num"), m.group("score")


def is_new_message_line(line):
    """
    Determines if the message constitutes the first line of a message or not,
    in which case it would be a 'body' message.
    """
    return bool(re.match(BEGIN_RE, line))
