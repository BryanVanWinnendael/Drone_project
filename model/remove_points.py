import open3d as o3d
import numpy as np
import os
import pandas as pd
from scipy.spatial import ConvexHull

def constructNewClassifiedPointCloud():
        # Load in all point clouds
        pcds = []
        for file in os.listdir("data/planes"):
            if file.endswith(".ply"):
                print(file)
                pcd = o3d.io.read_point_cloud(f"data/planes/{file}")
                pcds.append(pcd)

        # Merge point clouds
        new_pcd = o3d.geometry.PointCloud()
        for pcd in pcds:
            new_pcd += pcd

        # Save point cloud
        o3d.io.write_point_cloud("data/results/result-classified.ply", new_pcd)

def deleteSegment(id):
        # Update CSV
        df = pd.read_csv("data/results/output.csv")
        df = df[df["Segment"] != id]
        df.to_csv("data/results/output.csv", index=False)

        # Delete PLY
        os.remove(f"data/planes/plane_{id}.ply")

def remove_points(file, remove_points, remove_segments):
    if len(remove_points) > 0:
        pcd = o3d.io.read_point_cloud(file)
        points = np.asarray(pcd.points)
        remove_points = np.asarray([point.coord for point in remove_points])
        indexes = [i for i in range(len(points)) if np.any(np.all(points[i] == remove_points, axis=1))] 
        new_points = np.delete(points, indexes, axis=0)
        new_points = new_points.tolist()

        surface_area = ConvexHull(new_points, qhull_options='QJ').area / 2
        seg_id = int(file.split("_")[1].split(".")[0])
        df = pd.read_csv("data/results/output.csv")
        df.loc[df.Segment == seg_id, 'Surface area'] = surface_area
        df.to_csv("data/results/output.csv", index=False)

        pcd.points = o3d.utility.Vector3dVector(new_points)
        pcd.paint_uniform_color(np.asarray(pcd.colors)[0])
        o3d.io.write_point_cloud(file, pcd)
    
    if len(remove_segments) > 0:
        for segment_id in remove_segments:
            deleteSegment(segment_id)

    constructNewClassifiedPointCloud()  