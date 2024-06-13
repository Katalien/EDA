import os

import matplotlib.pyplot as plt

#from DatasetProcessor import DatasetProcessor
from Visualizer.FeatureVisualizer import FeatureVisualizer
from Visualizer.VisualizationMethods import BarPlotVisualize, BoxPlotVisualize, HistogramVisualize, LinePlotVisualize,\
                                    ScatterPlotVisualize, DensityPlotVisualize, PiePlotVisualize
from ConfigReader import ConfigReader
from utils import buildFeatures, ClassNamesDict
from PdfWriter import PdfWriter
from FeatureAnalysis import ContrastAnalysis, BrightnessAnalysis
from FeatureAnalysis import FeatureData


if __name__ == "__main__":
    # process config file
    # config_path = "config.yaml"
    # config_processor = ConfigReader(config_path)
    # images_path = config_processor.get_images_path()
    # output_path = config_processor.get_output_path()
    # if not os.path.exists(output_path):
    #     os.makedirs(output_path)
    # features_config = config_processor.get_features_config()
    # print(features_config)
    #
    # # extract classes to use
    # features2analyse = buildFeatures(features_config)
    # analyzers = list(features2analyse.keys())
    # class_analyzers = [ClassNamesDict.ClassNamesDict[analyzer] for analyzer in analyzers]
    #
    # # create dataset processor for data analysis
    # dataset_processor = DatasetProcessor('../dataset/images', class_analyzers)
    # features_map = dataset_processor.get_features()
    #
    # # create visualization plots
    # plots = []
    # for key, val in features_map.items():
    #     visualize_methods = list(features_config[key])
    #     for method in visualize_methods:
    #         feature_data = val
    #         visualizer = FeatureVisualizer(feature_data)
    #         plots.append(visualizer.visualize(method, str(key), "x", "y"))
    #
    #
    # # write to pdf
    # # PdfWriter.writePdf(plots, output_path)
    # for plot in plots:
    #     plt.show()

    # path = "../dataset/images/"
    # analyzer = ContrastAnalysis(path)
    # analyzer2 = BrightnessAnalysis(path)
    # feature = analyzer.get_feature()
    # feature2 = analyzer2.get_feature()

    # data = {
    #     'r': {'x': [1, 2, 3, 4, 5], 'y': [1, 4, 9, 16, 25]},
    #     'g': {'x': [1, 2, 3, 4, 5], 'y': [1, 8, 27, 64, 125]}
    # }
    #
    # feature = FeatureData("rgb", data)

    # visualizer = LinePlotVisualize()
    # visualizer.visualize(feature)
    #
    # visualizer1 = BarPlotVisualize()
    # plot2 = visualizer1.visualize(feature)

    # visualizer2 = BoxPlotVisualize()
    # plot2 = visualizer2.visualize(feature)

    # visualizer3 = HistogramVisualize()
    # plot2 = visualizer3.visualize(feature)
    #
    # visualizer1 = ScatterPlotVisualize()
    # plot2 = visualizer1.visualize(feature)
    #
    # visualizer = DensityPlotVisualize()
    # visualizer.visualize(feature)

    visualizer = PiePlotVisualize()
    visualizer.visualize(feature)
