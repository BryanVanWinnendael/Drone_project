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
        min_points = int(self.settings["Minimum points"])
        iterations = int(self.settings["Iterations * 100"] * 100)
        max_loops = int(self.settings["Maximum number of loops"])
        neighbours = int(self.settings["Number of neigbours"])
        voxel_size = self.settings["Voxel size"]
        treshold = self.settings["Treshold"]
        min_std_ratio = self.settings["Standard deviation ratio"]
        min_ratio = self.settings["Minimum ratio"]
        

        SegmentPointCloud(filename, self.waitingScreen, cluster=cluster_strategy, min_points=min_points, iterations=iterations, max_loops=max_loops, neighbours=neighbours, voxel_size=voxel_size, treshold=treshold, min_std_ratio=min_std_ratio, min_ratio=min_ratio)
