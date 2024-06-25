from DatasetProcessor import Manager
from DatasetProcessor import DatasetInfo

from FeatureAnalysis.LabeledFeatures import ClassesFrequencyAnalysis
from Visualizer.VisualizationMethods import BarPlotVisualizer
from FeatureAnalysis import FeatureData
import os





if __name__ == "__main__":
    # manager = Manager.Manager("config2.yaml")
    # manager.run()
    di = DatasetInfo.DatasetInfo("../dataset/real_dataset/")
    di.fill_info()










