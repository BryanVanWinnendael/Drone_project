from scipy.spatial import ConvexHull
import open3d as o3d
import numpy as np
import os
import csv
import pandas as pd

def CalculateSurfaces(strategy, waitingScreen):
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
            surface_area = CalculateSurfaceMeshPoissonMethod(pcd)
        elif strategy == "mesh_ball_pivoting":
            surface_area = CalculateSurfaceMeshBallPivotingMethod(pcd)
        else:
            surface_area = CalculateSurfaceConvexHull(pcd)

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


def CalculateSurfaceMeshPoissonMethod(pcd):
    # Estimate normals for the point cloud
    pcd.estimate_normals()

    # Create a mesh using Poisson
    mesh, _ = o3d.geometry.TriangleMesh.create_from_point_cloud_poisson(pcd, depth=3)

    # Get surface area
    return mesh.get_surface_area()

def CalculateSurfaceMeshBallPivotingMethod(pcd):
    # Estimate normals for the point cloud
    pcd.estimate_normals()

    # Create a mesh from the point cloud, with ball pivoting
    radii = [0.005, 0.01, 0.02, 0.04]
    mesh = o3d.geometry.TriangleMesh.create_from_point_cloud_ball_pivoting(
        pcd, o3d.utility.DoubleVector(radii))

    # Get surface area
    return mesh.get_surface_area()

def CalculateSurfaceConvexHull(pcd):
    points = np.asarray(pcd.points)

    # Calculate surface area
    return ConvexHull(points, qhull_options='QJ').area / 2


# Legacy code
# def OldCalculateSurfaces():
#     results = {}
#     # Check if directory exists, if not create it
#     if not os.path.exists("data/meshes"):
#         os.makedirs("data/meshes")

#     # Iterate over all files in directory
#     for i, filename in enumerate(os.listdir("data/meshes")):
#         file_path = os.path.join("data/meshes", filename)

#         if os.path.isfile(file_path):
#             # Load mesh from file
#             mesh = o3d.io.read_triangle_mesh(file_path)

#             # Compute the surface area
#             surface_area = mesh.get_surface_area()

#             results[i + 1] = surface_area

#     if not os.path.exists("data/results"):
#             os.makedirs("data/results")

#     # Add surface to csv
#     with open('data/results/planes.csv', 'r', newline='') as read_obj, \
#             open('data/results/output.csv', 'w', newline='') as write_obj:
#                 # Create a csv.reader object from the input file object
#                 reader = csv.reader(read_obj)
#                 # Create a csv.writer object from the output file object
#                 writer = csv.writer(write_obj)
#                 # Read each row of the input csv file as list
#                 for row in reader:
#                     # Append the default text in the row / list
#                     if row[0].isnumeric():
#                         row.append(results[int(row[0])])
#                     # Add the updated row / list to the output file
#                     writer.writerow(row)

#     # Delete planes.csv file
#     os.remove('data/results/planes.csv')
