import open3d as o3d
import numpy as np
from csv import writer
import os
from model.model_utils import reassignSegmentIds, constructNewClassifiedPointCloud, deleteSegment, calculateArea

class Merger():
    def __init__(self, parent):
        self.parent = parent
        self.ids = []

    def mergeSegments(self, ids, fileName=None):
        self.ids = ids
        selected_points = self.parent.getSelectedPoints()
        if len(self.ids) < 2 and len(selected_points) == 0:
            print("Select at least 2 segments to merge")
        else:
            # Create new point cloud
            new_pcd = o3d.geometry.PointCloud()
            points = [point.coord for point in selected_points]
            if fileName is not None and len(points) > 0:
                self.removePointsFromPointCloud(fileName, points)

            # Add points from all selected segments to new point cloud
            self.parent.clearSelectedPoints()
            for seg_id in self.ids:
                if os.path.isfile(f"data/planes/plane_{seg_id}.ply"):
                    pcd = o3d.io.read_point_cloud(f"data/planes/plane_{seg_id}.ply")
                    for point in np.asarray(pcd.points):
                        points.append(point)

                    # Delete the segments
                    deleteSegment(seg_id)

            new_pcd.points = o3d.utility.Vector3dVector(points)

            # Calculate new surface
            surface_area = calculateArea(points)

            color = list(np.random.choice(range(256), size=3))
            new_pcd.paint_uniform_color([color[0] / 255, color[1] / 255, color[2] / 255])
            self.saveSegment(new_pcd, surface_area, color)

            # Update the classified point cloud
            constructNewClassifiedPointCloud()
            self.parent.classifiedResultChanged()

            # Update the ids
            reassignSegmentIds()

    def saveSegment(self, pcd, surface_area, rgb):  
        print("Saving...")      
        with open("data/results/output.csv", "r") as f:
            last_id = f.readlines()[-1].split(",")[0]
            if last_id == "Segment":
                new_id = 1
            else:
                new_id = int(last_id) + 1
            f.close()

        o3d.io.write_point_cloud(f"data/planes/plane_{new_id}.ply", pcd)

        with open("data/results/output.csv", "a", newline='') as f: 
            writer_object = writer(f)
            str_ids = [str(seg_id) for seg_id in self.ids]
            class_name = "MERGED_" + '_'.join(str_ids)
            writer_object.writerow([new_id, class_name, surface_area, rgb])
            f.close()

    def removePointsFromPointCloud(self, fileName, points_to_remove):
        pcd = o3d.io.read_point_cloud(fileName)
        pc_points = np.asarray(pcd.points)
        points_to_mask = np.asarray(points_to_remove)  
        indexes = [i for i in range(len(pc_points)) if np.any(np.all(pc_points[i] == points_to_mask, axis=1))] 
        new_points = np.delete(pc_points, indexes, axis=0)
        new_points = new_points.tolist()
        pcd.points = o3d.utility.Vector3dVector(new_points)
        pcd.paint_uniform_color(np.asarray(pcd.colors)[0])
        o3d.io.write_point_cloud(fileName, pcd)