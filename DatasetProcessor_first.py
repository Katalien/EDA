# import os
# from ConfigReader import ConfigReader
# class Manager:
#     def __init__(self, config_path: str = "./config.yaml"):
#         self.config_path = config_path
#     def _read_pdf(self):
#         config_processor = ConfigReader(self.config_path)
#         images_path = config_processor.get_images_path()
#         output_path = config_processor.get_output_path()
#         if not os.path.exists(output_path):
#             os.makedirs(output_path)
#         features_config = config_processor.get_features_config()
