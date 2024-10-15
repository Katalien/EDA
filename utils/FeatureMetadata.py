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


FeatureDescriptions = {
    "Brightness": "Overall brightness for all images in the dataset",
    "Contrast": "Overall contrast for all images in the dataset",
    "AspectRatio": "Overall aspect ratio for all images in the dataset. (image height / image width)",
    "MaskedBrightness": "Masked segments brightness",
    "MaskedContrast": "Masked segments contrast",
    "MaskedGradient": "Masked segments gradient",
    "InstancesPerImage": "Amount of classes instances per image",
    "ClassesArea": "Area of classes segments, pxls",
    "ClassesBbAspectRatio": "Aspect ratio of classes bounging boxes",
    "ClassesDiameter": "Diameter of classes segments, pxls",
    "Class2ImageRatio": "The ratio of the defect area to the area of the entire image",
    "Color": "RGB channels' analysis of images in dataset. Values are normalized"
}