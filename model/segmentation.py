import os
from model.plane_detection.plane_detection import DetectPlanes
from model.plane_detection.surface_calculator import CalculateSurfaces
from model.view_data import ViewPointCloud, ViewMesh, ViewResult



def SegmentPointCloud(filename, waitingScreen, cluster=None, min_points=100, iterations=1000, max_loops=100, neighbours=20, voxel_size=0.01, treshold=0.01, min_std_ratio=2.0, min_ratio=0.05):
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
    DetectPlanes(filename, waitingScreen, cluster=cluster, min_points=min_points, iterations=iterations, max_loops=max_loops, neighbours=neighbours, voxel_size=voxel_size, treshold=treshold, min_std_ratio=min_std_ratio, min_ratio=min_ratio)

    print("Calculating surface areas...")
    CalculateSurfaces(waitingScreen)