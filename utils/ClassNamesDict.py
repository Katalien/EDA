from FeatureAnalysis import BrightnessAnalysis, ContrastAnalysis, AspectRatioAnalysis, ColorAnalysis, \
                            ClassesFrequencyAnalysis, PrecisionAnalysis, RecallAnalysis, LocationsMap, \
                            InstancePerImageAnalysis, ChanelSplitAnalysis, ClassesSquareAnalysis, \
                            ClassesBbAspectRatioAnalysis, ClassesDiameterAnalysis,\
                            MaskedBrightnessAnalysis, MaskedContrastAnalysis, MaskedGradientAnalysis
from Visualizer.VisualizationMethods import BarPlotVisualizer, BoxPlotVisualizer, DensityPlotVisualizer, \
                                            HistogramVisualizer, LinePlotVisualizer, ScatterPlotVisualizer,\
                                            ViolinPlotVisualizer



AnalysersClassNamesDict = {
    "Brightness": BrightnessAnalysis,
    "Contrast": ContrastAnalysis,
    "AspectRatio": AspectRatioAnalysis,
    "Color": ColorAnalysis,
    "ClassesFrequency": ClassesFrequencyAnalysis.ClassesFrequencyAnalysis,
    "Precision": PrecisionAnalysis.PrecisionAnalysis,
    "Recall": RecallAnalysis.RecallAnalysis,
    "LocationsMap": LocationsMap.LocationsMap,
    "InstancesPerImage": InstancePerImageAnalysis.InstancePerImageAnalysis,
    "ChanelSplitAnalysis": ChanelSplitAnalysis.ChanelSplitAnalysis,
    "ClassesSquareAnalysis": ClassesSquareAnalysis.ClassesSquareAnalysis,
    "ClassesBbAspectRatioAnalysis": ClassesBbAspectRatioAnalysis.ClassesBbAspectRatioAnalysis,
    "ClassesDiameterAnalysis": ClassesDiameterAnalysis.ClassesDiameterAnalysis,
    "MaskedBrightness": MaskedBrightnessAnalysis.MaskedBrightnessAnalysis,
    "MaskedContrast": MaskedContrastAnalysis.MaskedContrastAnalysis,
    "MaskedGradient": MaskedGradientAnalysis.MaskedGradientAnalysis
}

VisualizersClassNamesDict = {
    "bar": BarPlotVisualizer,
    "boxplot": BoxPlotVisualizer,
    "density": DensityPlotVisualizer,
    "histogram": HistogramVisualizer,
    "line": LinePlotVisualizer,
    "scatter": ScatterPlotVisualizer,
    "violin": ViolinPlotVisualizer
}

FeatureFolderDict = {
    "Color": ["images"],
    "AspectRatio": ["images"],
    "Brightness": ["images"],
    "Contrast": ["images"],
    "ClassesFrequency": ["labels"],
    "Precision": ["masks", "predictions"],
    "Recall": ["masks", "predictions"],
    "LocationsMap": ["masks"],
    "InstancesPerImage": ["labels"]
}