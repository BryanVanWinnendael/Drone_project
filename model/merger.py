import open3d as o3d
import numpy as np
from csv import writer
from model.plane_detection.color_generator import GenerateColors
from scipy.spatial import ConvexHull

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

        colors = GenerateColors(1)
        new_pcd.paint_uniform_color([colors[0][0] / 255, colors[0][1] / 255, colors[0][2] / 255])
        self.saveSegment(new_pcd, surface_area, [colors[0][0], colors[0][1], colors[0][2]])

    def saveSegment(self, pcd, surface_area, rgb):
        with open("data/results/output.csv", "r") as f1:
            last_id = f1.readlines()[-1].split(",")[0]
            new_id = int(last_id) + 1
            f1.close()

        o3d.io.write_point_cloud(f"data/planes/plane_{new_id}.ply", pcd)

        with open("data/results/output.csv", "a") as f: 
            writer_object = writer(f)
            writer_object.writerow([new_id, surface_area, rgb])
            f.close()