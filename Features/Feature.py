from abc import ABC, abstractmethod

class Feature(ABC):
    @abstractmethod
    def calculate(self, sample) -> float:
        pass


