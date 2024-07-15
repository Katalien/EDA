from FeatureAnalysis import BrightnessAnalysis, ContrastAnalysis, AspectRatioAnalysis, ColorAnalysis, \
    PrecisionAnalysis, RecallAnalysis
from FeatureAnalysis.GeneralFeatures.AtributesFeatures import ClassesBbAspectRatioAnalysis, ClassesAreaAnalysis, \
    Class2ImageRatioAnalysis
from FeatureAnalysis.GeneralFeatures.AtributesFeatures import ClassesDiameterAnalysis
from FeatureAnalysis.GeneralFeatures.LabelesFeatures import LocationsMap, InstancePerImageAnalysis, \
    ClassesFrequencyAnalysis
from FeatureAnalysis.GeneralFeatures.MaskedSegmentsAnalysis import MaskedBrightnessAnalysis, MaskedContrastAnalysis,\
                                                            MaskedGradientAnalysis
from FeatureAnalysis.GeneralFeatures.ImagesFeatures import ChanelSplitAnalysis
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
    "ClassesAreaAnalysis": ClassesAreaAnalysis.ClassesAreaAnalysis,
    "ClassesBbAspectRatioAnalysis": ClassesBbAspectRatioAnalysis.ClassesBbAspectRatioAnalysis,
    "ClassesDiameterAnalysis": ClassesDiameterAnalysis.ClassesDiameterAnalysis,
    "Class2ImageRatioAnalysis": Class2ImageRatioAnalysis.Class2ImageRatioAnalysis,
    "MaskedBrightnessAnalysis": MaskedBrightnessAnalysis.MaskedBrightnessAnalysis,
    "MaskedContrastAnalysis": MaskedContrastAnalysis.MaskedContrastAnalysis,
    "MaskedGradientAnalysis": MaskedGradientAnalysis.MaskedGradientAnalysis
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