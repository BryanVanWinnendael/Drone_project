import os
from model.plane_detection.plane_detection import DetectPlanes
from model.plane_detection.surface_calculator import CalculateSurfaces
from model.view_data import ViewPointCloud, ViewMesh, ViewResult



def SegmentPointCloud(filename, waitingScreen):
    # Check if the file exists
    print("Checking if the file exists...")
    if not os.path.exists(filename):
        print(f"The file {filename} does not exists")
        exit(1)

    print("Preparing project...")

    # Make the necessary directories
    print("Making the necessary directories...")
    if not os.path.exists("data/planes"):
        os.makedirs("data/planes")
    if not os.path.exists("data/results"):
        os.makedirs("data/results")

    print("Detecting planes...")
    DetectPlanes(filename, waitingScreen, cluster=True, min_points=200)

    print("Calculating surface areas...")
    CalculateSurfaces(waitingScreen)