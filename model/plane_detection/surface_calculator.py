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

    # Add surface to csv
    with open('data/results/planes.csv', 'r', newline='') as read_obj, \
            open('data/results/output.csv', 'w', newline='') as write_obj:
                # Create a csv.reader object from the input file object
                reader = csv.reader(read_obj)
                # Create a csv.writer object from the output file object
                writer = csv.writer(write_obj)
                # Read each row of the input csv file as list
                for row in reader:
                    # Append the default text in the row / list
                    if row[0].isnumeric():
                        row.append(results[int(row[0])])
                    # Add the updated row / list to the output file
                    writer.writerow(row)

    # Delete planes.csv file
    os.remove('data/results/planes.csv')