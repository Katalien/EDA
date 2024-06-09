import os
from DatasetProcessor import DatasetProcessor
from Visualizer.FeatureVisualizer import FeatureVisualizer
from ConfigReader import ConfigReader
from utils import buildFeatures, ClassNamesDict
from PdfWriter import PdfWriter


if __name__ == "__main__":
    config_path = "config.yaml"
    config_processor = ConfigReader(config_path)
    images_path = config_processor.get_images_path()
    output_path = config_processor.get_output_path()
    if not os.path.exists(output_path):
        os.makedirs(output_path)
    features_config = config_processor.get_features_config()
    print(features_config)

    features2analyse = buildFeatures(features_config)
    analyzers = list(features2analyse.keys())
    class_analyzers = [ClassNamesDict.ClassNamesDict[analyzer] for analyzer in analyzers]

    dataset_processor = DatasetProcessor('../dataset/images', class_analyzers)
    features_map = dataset_processor.get_features()
    print(features_map)

    plots = []

    for key, val in features_map.items():
        visualize_methods = list(features_config[key])
        for method in visualize_methods:
            feature_data = val
            visualizer = FeatureVisualizer(feature_data)
            plots.append(visualizer.visualize(method, str(key), "x", "y"))

    PdfWriter.writePdf(plots, output_path)


