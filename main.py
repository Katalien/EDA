from FeatureExtractor import BrightnessExtractor, ContrastExtractor, AspectRatioExtractor
from DatasetProcessor import DatasetProcessor

if __name__ == "__main__":
    extractors = [BrightnessExtractor, ContrastExtractor, AspectRatioExtractor]
    dataset_processor = DatasetProcessor('../dataset/images', extractors)
    features_map = dataset_processor.get_features()
    print(features_map)
