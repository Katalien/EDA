from abc import ABC, abstractmethod
from PIL import Image
from typing import Any, Dict
import numpy as np

class FeatureAnalysis(ABC):
    @abstractmethod
    def extract(self, image: Image.Image) -> Any:
        pass