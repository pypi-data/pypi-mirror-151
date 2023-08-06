from collections.abc import Callable

from wordleparse.printers.printers import GamePrinter, extract_person
from wordleparse.message import Message


def print_fn(messages: list[Message], ljust: int, fn: Callable = print) -> None:
    person = extract_person(messages)
    fails = [m for m in messages if "/" in m.score]
    success = [int(m.score) for m in messages if m not in fails]
    avg = (
        f"Average guesses left: {sum(success) / len(success):.1f} "
        if len(success) > 0
        else "No average guesses left "
    )
    fn(
        f"{person.ljust(ljust)}: {len(messages)} games, {len(fails)} failed attempts "
        + f"({len(fails) / len(messages):.1%}). "
        + avg
        + "for the completed games."
    )


squardle_printer: GamePrinter = GamePrinter("Squardle", print_fn)
