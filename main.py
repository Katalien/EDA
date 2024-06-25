from DatasetProcessor import Manager, DatasetManager
from FeatureAnalysis.LabeledFeatures import ClassesFrequencyAnalysis
from Visualizer.VisualizationMethods import BarPlotVisualizer
from FeatureAnalysis import FeatureData
import os





if __name__ == "__main__":
    manager = DatasetManager.DatasetManager("./config/config.yaml")
    manager.run()











