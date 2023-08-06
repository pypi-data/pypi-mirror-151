from typing import List, Callable

from wordleparse.printers.printers import GamePrinter, extract_person
from wordleparse.message import Message


def print_fn(messages: List[Message], ljust: int, fn: Callable = print) -> None:
    person = extract_person(messages)
    fails = [m for m in messages if "/" in m.score]
    success = [int(m.score) for m in messages if m not in fails]
    fn(
        f"{person.ljust(ljust)}: {len(messages)} games, {len(fails)} failed attempts. "
        + f"Average guesses left: {sum(success) / len(success):.1f} "
        + "for the completed games."
    )


squardle_printer = GamePrinter("Squardle", print_fn)
