from abc import ABC, abstractmethod
from typing import Union
import numpy as np


class FeatureAnalysis(ABC):

    def __init__(self, path: str):
        self.path = path

    @abstractmethod
    def _process_dataset(self) :
        pass

    @abstractmethod
    def _process_one_sample(self, sample: Union[np.ndarray, str], pred: Union[None, np.ndarray, str] = None):
        pass

    @abstractmethod
    def get_feature(self):
        pass