from dataclasses import dataclass


@dataclass
class Message:
    date: str
    person: str
    game: str
    number: str
    score: str
