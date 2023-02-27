from model.plane_detection.plane_detection import DetectPlanes
from model.plane_detection.plane_to_mesh import PlanesToMeshes
from model.plane_detection.surface_calculator import CalculateSurfaces
from model.view_data import ViewPointCloud, ViewMesh, ViewResult
from model.segmentation import SegmentPointCloud

class Segmentator:
    def __init__(self, waitingScreen):
        self.waitingScreen = waitingScreen

    def segment(self, filename):
        SegmentPointCloud(filename, 4, self.waitingScreen)
