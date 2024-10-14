# from typing import Dict, List
#
# class FeatureSummary():
#     def __init__(self, feature_name, values:Dict|List, visual_methods):
#         self.feature_name = feature_name
#         self.feature_type = self.__get_feature_type()
#         self.values = values
#         self.visual_methods = visual_methods
#
#     def __get_feature_type(self):
#         if isinstance(self.values[0], float):
#             return "GENERAL"
#         elif isinstance(self.values[0], list):
#             if isinstance(self.values[0][0], float):
#                 return "MASK"
#             else:
#                 raise KeyError(f"{self.feature_name} not GENERAL, not MASK")
#
#
#     def process_feature(self):
#         pass