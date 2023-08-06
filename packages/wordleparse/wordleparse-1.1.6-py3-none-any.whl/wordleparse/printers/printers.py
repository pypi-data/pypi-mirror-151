import re
from collections.abc import Callable, Iterator

from wordleparse.message import Message


DEFAULT_SCORE = r"(?P<score>[0-9X]+)/[0-9]+"


def default_print(messages: list[Message], ljust: int, fn: Callable = print) -> None:
    person = extract_person(messages)
    scores = list(_extract_scores(messages))
    fails = len([s for s in scores if s == "X"])
    success = [int(s) for s in scores if s != "X"]
    avg_score = (
        f"Average score: {sum(success) / len(success):.2f} "
        if len(success) > 0
        else "No average score "
    )
    fn(
        f"{person.ljust(ljust)}: {len(messages)} games, "
        + f"{fails} failed attempts ({fails / len(messages):.1%}). "
        + avg_score
        + "for the completed games."
    )


def extract_person(messages: list[Message]) -> str:
    persons = {m.person for m in messages}
    if len(persons) > 1:
        raise ValueError("Should only print messages of one person")

    return persons.pop()


def _extract_scores(messages: list[Message]) -> Iterator[str]:
    for msg in messages:
        m = re.match(DEFAULT_SCORE, msg.score)

        if m is not None:
            yield m.group("score")


class GamePrinter:
    game: str
    print_fn: Callable

    def __init__(self, game: str, print_fn: Callable = default_print):
        self.game = game
        setattr(self, "print_fn", print_fn)

    def print(self, messages: list[Message], ljust: int) -> None:
        print(f"Showing stats for {self.game}")
        persons = {m.person for m in messages}
        for person in sorted(persons):
            person_messages = [m for m in messages if m.person == person]
            self.print_fn(person_messages, ljust)

        print("=====================\n")

    def __repr__(self):
        return f"<GamePrinter for {self.game}>"
