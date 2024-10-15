from abc import ABC, abstractmethod


class Feature(ABC):
    """
    Class for processing one specific feature for given image/masks
    """
    @abstractmethod
    def calculate(self, sample) -> float:
        pass


