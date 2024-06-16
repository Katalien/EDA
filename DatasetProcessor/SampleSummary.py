class SampleSummary:
    def __init__(self, features, plots, sample_tag):
        self.features = features
        self.plots = plots
        if sample_tag not in ["train", "val", "test", ""]:
            raise ValueError("Incorrect sample tag. Carrect ones are: train, val, test, ''")
        self.sample_tag = sample_tag

