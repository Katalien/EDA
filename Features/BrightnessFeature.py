from .Feature import Feature

class BrightnessFeature(Feature):
    def calculate(self, sample) -> dict:
        image = sample.load_image()
        return {"General": self.calculate_brightness(image)}

    def calculate_brightness(self, image):
        return image.mean()