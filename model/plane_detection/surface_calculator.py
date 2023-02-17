import open3d as o3d
import numpy as np
import os
import csv

def CalculateSurfaces():
    results = {}
    # Check if directory exists, if not create it
    if not os.path.exists("data/meshes"):
        os.makedirs("data/meshes")

    # Iterate over all files in directory
    for i, filename in enumerate(os.listdir("data/meshes")):
        file_path = os.path.join("data/meshes", filename)

        if os.path.isfile(file_path):
            # Load mesh from file
            mesh = o3d.io.read_triangle_mesh(file_path)

            # Compute the surface area
            surface_area = mesh.get_surface_area()

            results[i + 1] = surface_area

    if not os.path.exists("data/results"):
            os.makedirs("data/results")

    with open('data/results/output.csv', mode='w') as file:
        writer = csv.writer(file)
        writer.writerow(['Segment', 'Surface area']) # Write header row
        for key, value in results.items():
            writer.writerow([key, value])
        print("Successfully wrote results to file: output.csv")