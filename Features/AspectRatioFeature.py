from .Feature import Feature

class AspectRatioFeature(Feature):
    def calculate(self, sample) -> float:
        image = sample.load_image()
        height, width = image.shape[:2]
        return width / height
