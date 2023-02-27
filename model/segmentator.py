from model.plane_detection.plane_detection import DetectPlanes
from model.plane_detection.plane_to_mesh import PlanesToMeshes
from model.plane_detection.surface_calculator import CalculateSurfaces
from model.view_data import ViewPointCloud, ViewMesh, ViewResult
from model.segmentation import SegmentPointCloud

class Segmentator:
    def __init__(self, waitingScreen, settings):
        self.waitingScreen = waitingScreen
        self.settings = settings

    def segment(self, filename):
        print(self.settings)

        cluster_strategy = self.settings["Cluster strategy"]
        treshold = self.settings["Treshold"]
        neighbours = self.settings["Number of neigbours"]
        # radius = self.settings["Radius"]
        min_points = self.settings["Min. points"]
        min_ratio = self.settings["Min. ratio"]

        print(cluster_strategy)
        print(treshold)

        SegmentPointCloud(filename, self.waitingScreen, cluster=cluster_strategy, treshold=treshold, neighbours=neighbours, min_points=min_points, min_ratio=min_ratio)
