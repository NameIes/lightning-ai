from typing import Any
from utils.singleton import SingletonMeta


class Storage(metaclass=SingletonMeta):
    def __init__(self) -> None:
        self._data: dict = {
            'lightning_started': False,
            'team': 'off',
            'round_playing': False,
        }

    def __getitem__(self, key: Any) -> Any:
        return self._data[key]

    def __setitem__(self, key: Any, value: Any) -> None:
        self._data[key] = value
