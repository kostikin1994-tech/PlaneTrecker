from abc import ABC, abstractmethod


class AircraftProvider(ABC):

    @abstractmethod
    def get_aircraft(self, country: str):
        """Получает список самолётов по стране."""
        pass