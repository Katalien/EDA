from .Feature import Feature

class BrightnessFeature(Feature):
    def calculate(self, sample) -> float:
        image = sample.load_image()
        return self.calculate_brightness(image)

    def calculate_brightness(self, image):
        return image.mean()