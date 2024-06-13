from abc import ABC, abstractmethod
from PIL import Image
from typing import Any, Dict
import numpy as np


class FeatureAnalysis(ABC):

    def __init__(self, path: str):
        self.path = path

    @abstractmethod
    def _process_dataset(self) :
        pass

    @abstractmethod
    def _process_one_sample(self, sample: np.ndarray):
        pass

    @abstractmethod
    def get_feature(self):
        pass