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
