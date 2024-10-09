from .Feature import Feature

class ContrastFeature(Feature):
    def calculate(self, sample) -> float:
        image = sample.load_image()
        return self.calculate_contrast(image)

    def calculate_contrast(self, image):
        return image.std()