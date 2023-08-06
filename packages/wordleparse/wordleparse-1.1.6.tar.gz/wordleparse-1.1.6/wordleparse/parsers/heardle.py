import re
import emoji

from wordleparse.gameparser import GameParser
from wordleparse.parser import MessageParser
from wordleparse.errors import UnparsableError


heardle_re = r"#Heardle #(?P<num>[0-9]+)([\s\S]+)"
hoordle_re = r"#Hoordle #(?P<num>[0-9]+)([\s\S]+)"


class ListenParser(GameParser):
    regex: str

    def __init__(self, regex: str):
        self.regex = regex

    def parse_game(self, message: str) -> tuple[str, str]:
        num, rest = parse_num(self.regex, message)
        emojis = emoji.emoji_list(self._strip(rest))  # type: ignore
        for i, em in enumerate(emojis):
            if em["emoji"] == "🟩":
                return num, f"{i+1}/6"
        return num, "X/6"

    @staticmethod
    def _strip(message: str) -> str:
        result = message.strip().split("\n")[0]
        result = result.replace("🔈", "")
        result = result.replace("🔉", "")
        result = result.replace("🔊", "")
        result = result.replace("🔇", "")
        return result


def parse_num(regex: str, message: str) -> tuple[str, ...]:
    m = re.match(regex, message)

    if not m:
        raise UnparsableError()

    return m.groups()


heardle_parser: MessageParser = MessageParser("Heardle", ListenParser(heardle_re))
hoordle_parser: MessageParser = MessageParser("Hoordle", ListenParser(hoordle_re))
