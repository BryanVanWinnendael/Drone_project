from model.segmentation import segmentPointCloud

class Segmentator:
    def __init__(self, waitingScreen, settings):
        self.waitingScreen = waitingScreen
        self.settings = settings

    def segment(self, filename):
        cluster_strategy = self.settings["Cluster strategy"]
        surface_strategy = self.settings["Surface strategy"]

        segmentation_parameters = {
            "redistribute_smaller_clusters": self.settings["Redistribute smaller clusters"],
            "min_points": int(self.settings["Minimum points"]),
            "iterations": int(self.settings["Iterations"]),
            "max_loops": int(self.settings["Maximum number of loops"]),
            "neighbours": int(self.settings["Number of neighbours"]),
            "voxel_size": self.settings["Voxel size"],
            "treshold": self.settings["Treshold"],
            "min_std_ratio": self.settings["Standard deviation ratio"],
            "min_ratio": self.settings["Minimum ratio"],
            "epsilon": self.settings["Epsilon (DBSCAN)"],
            "number_of_clusters": int(self.settings["Number of Clusters (Agglomerative)"]),
        }

        segmentPointCloud(filename, self.waitingScreen, cluster=cluster_strategy, surface=surface_strategy, parameters=segmentation_parameters)
