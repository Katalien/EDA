from .Feature import Feature
import numpy as np

class ContrastFeature(Feature):
    def calculate(self, sample) -> dict:
        image = sample.load_image()
        return {"General": np.std(image)}
