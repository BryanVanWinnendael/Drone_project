import open3d as o3d
import numpy as np
from csv import writer, reader
from scipy.spatial import ConvexHull
import pandas as pd
class Merger():
    def __init__(self):
        pass

    def mergeSegments(self, ids):
        new_pcd = o3d.geometry.PointCloud()
        points = []
        for seg_id in ids:
            pcd = o3d.io.read_point_cloud(f"data/planes/plane_{seg_id}.ply")
            for point in np.asarray(pcd.points):
                points.append(point)

        new_pcd.points = o3d.utility.Vector3dVector(points)

        surface_area = ConvexHull(points, qhull_options='QJ').area / 2

        color = list(np.random.choice(range(256), size=3))
        new_pcd.paint_uniform_color([color[0] / 255, color[1] / 255, color[2] / 255])
        self.saveSegment(new_pcd, surface_area, color)

    def saveSegment(self, pcd, surface_area, rgb):  
        print("saving...")      
        with open("data/results/output.csv", "r") as f:
            last_id = f.readlines()[-1].split(",")[0]
            new_id = int(last_id) + 1
            f.close()

        o3d.io.write_point_cloud(f"data/planes/plane_{new_id}.ply", pcd)

        with open("data/results/output.csv", "a", newline='') as f: 
            writer_object = writer(f)
            writer_object.writerow([new_id, "MERGED" ,surface_area, rgb])
            f.close()
        