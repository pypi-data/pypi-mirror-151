from wordleparse.message import Message
from wordleparse.printers import GamePrinter, crosswordle_printer, squardle_printer

printers: list[GamePrinter] = [
    GamePrinter("Wordle"),
    GamePrinter("Woordle"),
    GamePrinter("Woordle6"),
    GamePrinter("Worldle"),
    GamePrinter("Primel"),
    GamePrinter("Letterle"),
    GamePrinter("Not Wordle"),
    GamePrinter("Nerdle"),
    GamePrinter("Vardle"),
    crosswordle_printer,
    squardle_printer,
    GamePrinter("Waffle"),
    GamePrinter("Heardle"),
    GamePrinter("Hoordle"),
]


def print_result(game: str, messages: list[Message]) -> None:
    try:
        printer: GamePrinter = [p for p in printers if p.game == game][0]
    except IndexError as e:
        raise ValueError(
            f"No valid printer found for game {game}. Known printers are {printers}"
        ) from e

    max_person_length = max([len(p) for p in {m.person for m in messages}])
    printer.print(messages, ljust=max_person_length)
