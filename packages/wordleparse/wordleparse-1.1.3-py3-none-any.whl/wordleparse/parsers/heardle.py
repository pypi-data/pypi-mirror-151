import re
import emoji

from wordleparse.parser import MessageParser, CustomParser
from wordleparse.errors import UnparsableError


heardle_re = r"#Heardle #(?P<score>[0-9]+)([\s\S]+)"
hoordle_re = r"#Hoordle #(?P<score>[0-9]+)([\s\S]+)"


class ListenParser:
    def __init__(self, regex):
        self.regex = regex

    def parse_game(self, message: str):
        score, rest = parse_score(self.regex, message)
        rest = rest.strip().split("\n")[0]
        rest = rest.replace("🔈", "")
        rest = rest.replace("🔉", "")
        rest = rest.replace("🔊", "")
        rest = rest.replace("🔇", "")
        rest = emoji.emoji_list(rest)
        for i, em in enumerate(rest):
            if em["emoji"] == "🟩":
                return score, f"{i+1}/6"
        return score, "X/6"


def parse_score(regex, message: str):
    m = re.match(regex, message)

    if not m:
        raise UnparsableError()

    return m.groups()


heardle_parser = MessageParser("Heardle", ListenParser(heardle_re))
hoordle_parser = MessageParser("Hoordle", ListenParser(hoordle_re))
