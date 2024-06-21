from typing import Any, Type
from abc import ABC, abstractmethod
from utils.singleton import SingletonMeta


class Observer(ABC):
    @abstractmethod
    def notify(self, data: dict) -> None:
        pass


class Storage(metaclass=SingletonMeta):
    def __init__(self) -> None:
        self.data: dict = {
            'lightning_started': False,
            'sensitivity': 0.5,
            'team': 0,
            'round_playing': False,
        }

        self._observers: list[Type[Observer]] = []

    def register_observer(self, observer: Type[Observer]) -> None:
        self._observers.append(observer)

    def set_data(self, key: Any, value: Any) -> None:
        self.data[key] = value
        for observer in self._observers:
            observer.notify(self.data)
