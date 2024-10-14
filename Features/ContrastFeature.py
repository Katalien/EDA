from .Feature import Feature

class ContrastFeature(Feature):
    def calculate(self, sample) -> dict:
        image = sample.load_image()
        return  {"General": self.calculate_contrast(image)}

    def calculate_contrast(self, image):
        return image.std()