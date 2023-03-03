import open3d as o3d
import numpy as np
import pandas as pd
from model.model_utils import constructNewClassifiedPointCloud, deleteSegment, reassignSegmentIds, calculateArea

def remove_points(file, remove_points, remove_segments):
    if len(remove_points) > 0:
        pcd = o3d.io.read_point_cloud(file)
        points = np.asarray(pcd.points)
        remove_points = np.asarray([point.coord for point in remove_points])
        indexes = [i for i in range(len(points)) if np.any(np.all(points[i] == remove_points, axis=1))] 
        new_points = np.delete(points, indexes, axis=0)
        new_points = new_points.tolist()

        if len(new_points) > 3:
            surface_area = calculateArea(new_points)
            seg_id = int(file.split("_")[1].split(".")[0])
            df = pd.read_csv("data/results/output.csv")
            df.loc[df.Segment == seg_id, 'Surface area'] = surface_area
            df.to_csv("data/results/output.csv", index=False)

            pcd.points = o3d.utility.Vector3dVector(new_points)
            pcd.paint_uniform_color(np.asarray(pcd.colors)[0])
            o3d.io.write_point_cloud(file, pcd)
        else:
            print("Deleting segment, reason: less than 4 points left")
            remove_segments.append(int(file.split("_")[1].split(".")[0]))

    if len(remove_segments) > 0:
        for segment_id in remove_segments:
            deleteSegment(segment_id)
        reassignSegmentIds()
    
    constructNewClassifiedPointCloud() 