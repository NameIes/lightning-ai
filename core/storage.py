from utils.singleton import SingletonMeta


class Storage(metaclass=SingletonMeta):
    def __init__(self) -> None:
        self.data = {
            'lightning_started': False,
            'sensitivity': 0.5,
            'team': 0,
            'round_playing': False,
        }

        self._observers = []

    def register_observer(self, observer):
        self._observers.append(observer)

    def set_data(self, key, value):
        self.data[key] = value
        for observer in self._observers:
            observer.notify(self.data)
