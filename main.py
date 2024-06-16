from DatasetProcessor import DatasetManager

from FeatureAnalysis.LabeledFeatures import ClassesFrequencyAnalysis
from Visualizer.VisualizationMethods import BarPlotVisualizer
from FeatureAnalysis import FeatureData


def test_func():
    d1 = {"skol": 3, "pori": 7, "sink": 1}
    d2 = {"skol": 10, "pori": 6, "sink": 3}
    data_dict1 = {"x": list(d1.keys()), "y": list(d1.values())}
    data_dict2 = {"x": list(d2.keys()), "y": list(d2.values())}
    feature1 = FeatureData("1", data_dict1)
    feature2 = FeatureData("2", data_dict2)

    feature_list = [feature1, feature2]
    visualizer = BarPlotVisualizer()
    visualizer.visualize(feature_list)

if __name__ == "__main__":
    manager = DatasetManager.Manager()
    manager.run()






