import os
import csv
import numpy as np
import pandas as pd
import open3d as o3d

from model.utils import calculateArea

def calculateSurfaces(strategy, waitingScreen):
    results = {}

    # Iterate over all files in directory
    waitingScreen.progress.emit("Calculating surface areas...")
    for filename in os.listdir("data/planes"):
        file_path = os.path.join("data/planes", filename)

        segment_number = filename.split(".")[0]
        segment_number = segment_number.split("_")[1]

        # Load pointcloud from file
        pcd = o3d.io.read_point_cloud(file_path)

        # Compute the surface area
        
        if strategy == "mesh_poisson":
            surface_area = calculateSurfaceMeshPoissonMethod(pcd)
        elif strategy == "mesh_ball_pivoting":
            surface_area = calculateSurfaceMeshBallPivotingMethod(pcd)
        else:
            surface_area = calculateArea(np.asarray(pcd.points))

        results[segment_number] = [surface_area, [int(x * 255) for x in np.asarray(pcd.colors)[0]]]

    # Write the results to a csv file
    print("Writing results to a csv file...")
    waitingScreen.progress.emit("Writing results to a csv file...")
    with open("data/results/output.csv", "w", newline='') as f:
        writer = csv.writer(f)
        writer.writerow(["Segment", "Class", "Surface area", "rgb"])
        for key, value in results.items():
            writer.writerow([key,"Unknown", value[0], value[1]])

    # Sort the csv file by segment number
    print("Sorting csv file...")
    waitingScreen.progress.emit("Sorting csv file...")
    
    df = pd.read_csv("data/results/output.csv")
    df = df.sort_values(by=["Segment"])
    df.to_csv("data/results/output.csv", index=False)


def calculateSurfaceMeshPoissonMethod(pcd):
    # Estimate normals for the point cloud
    pcd.estimate_normals()

    # Create a mesh using Poisson
    mesh, _ = o3d.geometry.TriangleMesh.create_from_point_cloud_poisson(pcd, depth=3)

    # Get surface area
    return mesh.get_surface_area()

def calculateSurfaceMeshBallPivotingMethod(pcd):
    # Estimate normals for the point cloud
    pcd.estimate_normals()

    # Create a mesh from the point cloud, with ball pivoting
    radii = [0.005, 0.01, 0.02, 0.04]
    mesh = o3d.geometry.TriangleMesh.create_from_point_cloud_ball_pivoting(
        pcd, o3d.utility.DoubleVector(radii))

    # Get surface area
    return mesh.get_surface_area()