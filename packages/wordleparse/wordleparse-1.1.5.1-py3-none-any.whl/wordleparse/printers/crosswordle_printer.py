import re
from typing import List, Callable

from wordleparse.printers.printers import GamePrinter, extract_person
from wordleparse.message import Message


def print_fn(messages: List[Message], ljust: int, fn: Callable = print) -> None:
    person = extract_person(messages)
    scores = [re.match(r"(?:([0-9]+)m )?([0-9]+)s", m.score).groups() for m in messages]
    seconds = sum(
        [int(s[0]) * 60 + int(s[1]) if s[0] is not None else int(s[1]) for s in scores]
    )
    fn(
        f"{person.ljust(ljust)}: {len(messages)} games, average time of "
        + f"{seconds / len(messages):.0f}s"
    )


crosswordle_printer = GamePrinter("Crosswordle", print_fn)
