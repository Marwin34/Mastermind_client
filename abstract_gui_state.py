from abc import ABC, abstractmethod


class GUIState(ABC):
    @abstractmethod
    def update(self, process):
        pass

    @abstractmethod
    def draw(self):
        pass

    @abstractmethod
    def set(self, identity, val):
        pass

    @abstractmethod
    def reset_input(self):
        pass

    @abstractmethod
    def reset_state(self):
        pass
