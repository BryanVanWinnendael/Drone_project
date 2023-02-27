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
        cluster_strategy = self.settings["Cluster strategy"]
        treshold = self.settings["Treshold"]
        neighbours = int(self.settings["Number of neigbours"])
        iterations = int(self.settings["Iterations * 100"] * 100)
        min_points = int(self.settings["Min. points"])
        min_ratio = self.settings["Min. ratio"]

        SegmentPointCloud(filename, self.waitingScreen, cluster=cluster_strategy, treshold=treshold, neighbours=neighbours, min_points=min_points, min_ratio=min_ratio, iterations=iterations)
