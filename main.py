from FeatureExtractor import BrightnessExtractor, ContrastExtractor, AspectRatioExtractor
from DatasetProcessor import DatasetProcessor
from Visualizer.FeatureVisualizer import FeatureVisualizer

if __name__ == "__main__":
    extractors = [BrightnessExtractor, ContrastExtractor, AspectRatioExtractor]
    dataset_processor = DatasetProcessor('../dataset/images', extractors)
    features_map = dataset_processor.get_features()
    print(features_map)

    for key, val in features_map.items():
        print(key)
        print(val)

        feature_data = val
        visualizer = FeatureVisualizer(feature_data)
        visualizer.visualize('line')
        visualizer.visualize('bar')

        print()


