import os
from typing import List

import matplotlib.pyplot as plt

#from DatasetProcessor import DatasetProcessor
from Visualizer.FeatureVisualizer import FeatureVisualizer
from Visualizer.VisualizationMethods import BarPlotVisualizer, BoxPlotVisualizer, HistogramVisualizer, LinePlotVisualizer,\
                                    ScatterPlotVisualizer, DensityPlotVisualizer, PiePlotVisualizer
from ConfigReader import ConfigReader
from utils import buildFeatures, ClassNamesDict
from PdfWriter import PdfWriter
from FeatureAnalysis import ContrastAnalysis, BrightnessAnalysis, ColorAnalysis
from FeatureAnalysis import FeatureData
import numpy as np

def run():
    config_path = "config.yaml"
    config_processor = ConfigReader(config_path)
    images_path = config_processor.get_images_path()
    output_path = config_processor.get_output_path()
    if not os.path.exists(output_path):
        os.makedirs(output_path)
    features_config = config_processor.get_features_config()
    features2analyse = buildFeatures(features_config)
    print(features2analyse)
    analyzers = list(features2analyse.keys())
    for analyzer, visual_methods in features2analyse.items():
        feature_analyzer = ClassNamesDict.AnalysersClassNamesDict[analyzer](images_path)
        features = feature_analyzer.get_feature()
        if type(features) is not List[FeatureData]:
            features = [features]
        for visual_method in visual_methods:
            visualizer = ClassNamesDict.VisualizersClassNamesDict[visual_method]()
            visualizer.visualize(features)





if __name__ == "__main__":
    # run()
    # # process config file
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







    path = "../dataset/test/"
    # analyzer = ContrastAnalysis(path)
    # analyzer2 = BrightnessAnalysis(path)
    analyzer3 = ColorAnalysis.ColorAnalysis(path)
    feature_list = analyzer3.get_feature()

    # feature_data1 = FeatureData(feature_name="Feature 1",
    #                             data={"x": list(range(10)), "y": np.random.randint(0, 100, 10)})
    # feature_data2 = FeatureData(feature_name="Feature 2",
    #                             data={"x": list(range(10)), "y": np.random.randint(0, 100, 10)})
    #
    # feature_list = [feature_data1, feature_data2]


    # visualizer = LinePlotVisualize()
    # visualizer.visualize(feature_list)
    #
    visualizer1 = HistogramVisualizer()
    plot2 = visualizer1.visualize(feature_list)
    #
    # visualizer2 = BoxPlotVisualize()
    # plot2 = visualizer2.visualize(feature_list)
    #
    # visualizer3 = BarPlotVisualize()
    # plot2 = visualizer3.visualize(feature_list)
    #
    # visualizer1 = ScatterPlotVisualize()
    # plot2 = visualizer1.visualize(feature_list)
    #
    # visualizer = DensityPlotVisualize()
    # visualizer.visualize(feature_list)


