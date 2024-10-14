from Features import BrightnessFeature, ContrastFeature, AspectRatioFeature, MaskedContrastFeature, \
    MaskedBrightnessFeature, MaskedGradientFeature, InstancePerImageFeature, ClassesAreaFeature, \
    ClassesBBAspectRatioFeature, ClassesDiameterFeature, Class2ImageRatioFeature
from Visualizer.VisualizationMethods import BarPlotVisualizer, BoxPlotVisualizer, DensityPlotVisualizer, \
                                            HistogramVisualizer, LinePlotVisualizer, ScatterPlotVisualizer,\
                                            ViolinPlotVisualizer

FeatureClasses = ["General", "Labels", "Attributes", "Masks", "Compare"]

FeatureClassDict = {
    "Brightness": BrightnessFeature.BrightnessFeature,
    "Contrast": ContrastFeature.ContrastFeature,
    "AspectRatio": AspectRatioFeature.AspectRatioFeature,
    "MaskedBrightness": MaskedBrightnessFeature.MaskedBrightnessFeature,
    "MaskedContrast": MaskedContrastFeature.MaskedContrastFeature,
    "MaskedGradient": MaskedGradientFeature.MaskedGradientFeature,
    "InstancesPerImage": InstancePerImageFeature.InstancePerImageFeature,
    "ClassesArea": ClassesAreaFeature.ClassesAreaFeature,
    "ClassesBbAspectRatio": ClassesBBAspectRatioFeature.ClassesBBAspectRatioFeature,
    "ClassesDiameter": ClassesDiameterFeature.ClassesDiameterFeature,
    "Class2ImageRatio":   Class2ImageRatioFeature.Class2ImageRatioFeature
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

GeneralFeatures = ["AspectRatio", "Brightness", "Color", "Contrast"]
LabeledFeatures = ["ClassesFrequency", "InstancesPerImage", "LocationMap", "ClassesArea",
                   "ClassesBbAspectRatio", "ClassesDiameter", "Class2ImageRatio"]
MaskedFeatures = ["MaskedContrast", "MaskedBrightness", "MaskedGradient"]
