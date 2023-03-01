import os
from model.plane_detection.plane_detection import DetectPlanes
from model.plane_detection.surface_calculator import CalculateSurfaces
from model.model_utils import GetDefaulftParameters

def SegmentPointCloud(filename, waitingScreen, cluster=None, parameters=GetDefaulftParameters()):
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
    DetectPlanes(filename, waitingScreen, cluster=cluster, parameters=parameters)

    print("Calculating surface areas...")
    CalculateSurfaces(waitingScreen)