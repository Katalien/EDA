import matplotlib.pyplot as plt
from .Visualizer import Visualizer
import seaborn as sns
import pandas as pd

class BoxPlotVisualizer(Visualizer):
    def visualize(self, feature_summary, grid=True):
        feature_data_list = feature_summary.features_list
        plt.figure(figsize=(12, 12))

        lengths = [len(feature_data.data["y"]) for feature_data in feature_data_list]
        all_same_length = all(length == lengths[0] for length in lengths)

        if all_same_length:
            data_dict = {feature_data.feature_name: feature_data.data["y"] for feature_data in feature_data_list}
            df = pd.DataFrame(data_dict)
        else:
            data = []
            for feature_data in feature_data_list:
                feature_name = feature_data.feature_name
                y_values = feature_data.data["y"]
                for y in y_values:
                    data.append({'class': feature_name, 'area': y})
            df = pd.DataFrame(data)

        # Calculate means for each class
        means = df.groupby('class')['area'].mean() if 'class' in df else df.mean()
        max_mean = max(means)
        min_mean = min(means)
        significant_difference = (max_mean / min_mean) > 10

        if significant_difference:
            # Create two subplots with separate y-axes
            fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 12))

            if 'class' in df:
                sns.boxplot(x='class', y='area', data=df[df['class'] == means.idxmax()], ax=ax1)
                sns.boxplot(x='class', y='area', data=df[df['class'] == means.idxmin()], ax=ax2)
            else:
                sns.boxplot(data=df[[means.idxmax()]], ax=ax1, orient="v")
                sns.boxplot(data=df[[means.idxmin()]], ax=ax2, orient="v")

            ax1.set_title(f"Boxplot of {means.idxmax()}", fontsize=14)
            ax2.set_title(f"Boxplot of {means.idxmin()}", fontsize=14)
            fig.suptitle(f"Boxplots of {feature_summary.feature_name}", fontsize=16, fontweight='bold')

            if grid:
                ax1.grid(True)
                ax2.grid(True)

            plt.tight_layout()
        else:
            if 'class' in df:
                sns.boxplot(x='class', y='area', data=df, orient="v")
            else:
                sns.boxplot(data=df, orient="v")

            plt.title(f"Box Plot of {feature_summary.feature_name}", fontsize=16, fontweight='bold')
            plt.xlabel('Feature')
            plt.ylabel('Value')

            if grid:
                plt.grid(True)

            plt.tight_layout()

        # plt.show()
        return plt.gcf()



    # def visualize(self, feature_summary: FeatureSummary, grid=True):
    #     feature_data_list = feature_summary.features_list
    #     plt.figure(figsize=(12, 12))
    #
    #     lengths = [len(feature_data.data["y"]) for feature_data in feature_data_list]
    #     all_same_length = all(length == lengths[0] for length in lengths)
    #     if all_same_length:
    #         data_dict = {feature_data.feature_name: feature_data.data["y"] for feature_data in feature_data_list}
    #         df = pd.DataFrame(data_dict)
    #         sns.boxplot(data=df, orient="v")
    #     else:
    #         data = []
    #         for feature_data in feature_data_list:
    #             feature_name = feature_data.feature_name
    #             y_values = feature_data.data["y"]
    #             for y in y_values:
    #                 data.append({'class': feature_name, 'area': y})
    #         df = pd.DataFrame(data)
    #         sns.boxplot(x='class', y='area', data=df)
    #
    #     plt.title(f"Box Plot of {feature_summary.feature_name}")
    #     plt.xlabel('Feature')
    #     plt.ylabel('Value')
    #
    #     if grid:
    #         plt.grid(True)
    #
    #     plt.tight_layout()
    #     # plt.show()
    #     return plt.gcf()