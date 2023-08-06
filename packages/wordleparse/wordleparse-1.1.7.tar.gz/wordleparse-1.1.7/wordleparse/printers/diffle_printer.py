import re
from collections.abc import Callable, Iterator

from wordleparse.printers.printers import GamePrinter, extract_person
from wordleparse.message import Message


def print_fn(messages: list[Message], ljust: int, fn: Callable = print) -> None:
    person = extract_person(messages)
    scores = _extract_scores(messages)
    avg_words, avg_letters = _compute_averages(scores)
    fn(
        f"{person.ljust(ljust)}: {len(messages)} games. "
        + f"Average words/letters left: {avg_words:.1f}/{avg_letters:.1f} "
        + "for the completed games."
    )


def _extract_scores(messages: list[Message]) -> Iterator[tuple[str, ...]]:
    for msg in messages:
        m = re.match(r"([0-9]+) words / ([0-9]+) letters", msg.score)

        if m is not None:
            yield m.groups()


def _compute_averages(scores: Iterator[tuple[str, ...]]) -> tuple[float, float]:
    tot_words = 0
    tot_letters = 0
    i = None
    for i, (words, letters) in enumerate(scores):
        tot_words += int(words)
        tot_letters += int(letters)

    i += 1 if i else 1

    return tot_words / i, tot_letters / i


diffle_printer: GamePrinter = GamePrinter("Diffle", print_fn)
