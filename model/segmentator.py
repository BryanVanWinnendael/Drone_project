from model.segmentation import SegmentPointCloud

class Segmentator:
    def __init__(self, waitingScreen, settings):
        self.waitingScreen = waitingScreen
        self.settings = settings

    def segment(self, filename):
        cluster_strategy = self.settings["Cluster strategy"]

        segmentation_parameters = {
            "min_points": int(self.settings["Minimum points"]),
            "iterations": int(self.settings["Iterations"]),
            "max_loops": int(self.settings["Maximum number of loops"]),
            "neighbours": int(self.settings["Number of neigbours"]),
            "voxel_size": self.settings["Voxel size"],
            "treshold": self.settings["Treshold"],
            "min_std_ratio": self.settings["Standard deviation ratio"],
            "min_ratio": self.settings["Minimum ratio"],
            "epsilon": self.settings["Epsilon (DBSCAN)"],
            "number_of_clusters": int(self.settings["Number of Clusters (Agglomerative)"]),
        }

        SegmentPointCloud(filename, self.waitingScreen, cluster=cluster_strategy, parameters=segmentation_parameters)
