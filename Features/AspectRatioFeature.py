from .Feature import Feature

class AspectRatioFeature(Feature):
    def calculate(self, sample) -> dict:
        image = sample.load_image()
        height, width = image.shape[:2]
        return {"General": width / height}
