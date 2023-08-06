from abc import ABC, abstractmethod


class GameParser(ABC):
    @abstractmethod
    def parse_game(self, message: str) -> tuple[str, str]:
        pass
