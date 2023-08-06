import re
from collections.abc import Iterator, Callable

from wordleparse.printers.printers import GamePrinter, extract_person
from wordleparse.message import Message


def print_fn(messages: list[Message], ljust: int, fn: Callable = print) -> None:
    person = extract_person(messages)
    scores = _extract_scores(messages)
    seconds = sum(
        [int(s[0]) * 60 + int(s[1]) if s[0] is not None else int(s[1]) for s in scores]
    )
    fn(
        f"{person.ljust(ljust)}: {len(messages)} games, average time of "
        + f"{seconds / len(messages):.0f}s"
    )


def _extract_scores(messages: list[Message]) -> Iterator[tuple[str, ...]]:
    for msg in messages:
        m = re.match(r"(?:([0-9]+)m )?([0-9]+)s", msg.score)

        if m is not None:
            yield m.groups()


crosswordle_printer: GamePrinter = GamePrinter("Crosswordle", print_fn)
