import os
from model.plane_detection.plane_detection import DetectPlanes
from model.plane_detection.surface_calculator import CalculateSurfaces
from model.model_utils import GetDefaulftParameters
import open3d as o3d

def SegmentPointCloud(filename, waitingScreen, cluster=None, surface="Convex Hull", parameters=GetDefaulftParameters()):
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
    
    # Save original point cloud
    print("Saving original point cloud...")
    pcd = o3d.io.read_point_cloud(filename)
    name = filename.split("/")[-1]
    newFilename = f"original_{name}"
    o3d.io.write_point_cloud(f"data/results/{newFilename}", pcd)

    print("Detecting planes...")
    DetectPlanes(filename, waitingScreen, cluster=cluster, parameters=parameters)

    print("Calculating surface areas...")
    CalculateSurfaces(surface, waitingScreen)