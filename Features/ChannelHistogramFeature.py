from .Feature import Feature
from matplotlib import pyplot as plt
import numpy as np


class ChannelsHistogramFeature(Feature):
    def calculate_channel_histogram(self, sample):
        colors = ("red", "green", "blue")
        fig, ax = plt.subplots()
        ax.set_xlim([0, 256])
        for channel_id, color in enumerate(colors):
            histogram, bin_edges = np.histogram(
                sample[:, :, channel_id], bins=256, range=(0, 256)
            )
            ax.plot(bin_edges[0:-1], histogram, color=color)

        ax.set_title("Color Histogram")
        ax.set_xlabel("Color value")
        ax.set_ylabel("Pixel count")
        plt.show()