from .Feature import Feature
import numpy as np


class BrightnessFeature(Feature):
    def calculate(self, sample) -> dict:
        image = sample.load_image()
        return {"General": np.mean(image)}
