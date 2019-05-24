from abc import ABC, abstractmethod


class GameState(ABC):
    @abstractmethod
    def update(self):
        pass

    @abstractmethod
    def draw(self):
        pass

    @abstractmethod
    def send(self):
        pass

    @abstractmethod
    def next(self):
        pass

    @abstractmethod
    def process_input(self, inputs):
        pass

    @abstractmethod
    def handle_events(self):
        pass

    @abstractmethod
    def reset_state(self):
        pass
