import json
from DatasetProcessor import DatasetInfo
from FeatureAnalysis import FeatureSummary

class JsonReader:
    def __init__(self, json_filepath: str):
        self.json_filepath = json_filepath

    def read_json(self):
        with open(self.json_filepath, "r") as json_file:
            data_json = json.load(json_file)
        dataset_info_dict = data_json["Dataset Info"]
        dataset_info = DatasetInfo.DatasetInfo.from_dict(dataset_info_dict)
        features_info_list = data_json["Features Info"]
        feature_summaries = []
        for feature_info_item in features_info_list:
            feature_summary = FeatureSummary.FeatureSummary.from_dict(feature_info_item)
            feature_summaries.append(feature_summary)
        return dataset_info, feature_summaries