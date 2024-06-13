from typing import Dict, List


def buildFeatures(features_config: Dict[str, List]) -> Dict[str, List]:
    features2analyze = {}
    for key, val in features_config.items():
        capitalKey = key.capitalize() + "Analysis"
        features2analyze[capitalKey] = list(val)
    return features2analyze
