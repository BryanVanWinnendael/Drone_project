import open3d as o3d
import numpy as np
from csv import writer, reader
from scipy.spatial import ConvexHull
import pandas as pd
import os
class Merger():
    def __init__(self, parent):
        self.parent = parent
        self.ids = []

    def mergeSegments(self, ids):
        self.ids = ids
        if len(self.ids) < 2:
            print("Select at least 2 segments to merge")
        else:
            # Create new point cloud
            new_pcd = o3d.geometry.PointCloud()
            
            # Add points from all selected segments to new point cloud
            points = []
            for seg_id in self.ids:
                if os.path.isfile(f"data/planes/plane_{seg_id}.ply"):
                    pcd = o3d.io.read_point_cloud(f"data/planes/plane_{seg_id}.ply")
                    for point in np.asarray(pcd.points):
                        points.append(point)

                    # Delete the segments
                    self.deleteSegment(seg_id)

            new_pcd.points = o3d.utility.Vector3dVector(points)

            # Calculate new surface
            surface_area = ConvexHull(points, qhull_options='QJ').area / 2

            color = list(np.random.choice(range(256), size=3))
            new_pcd.paint_uniform_color([color[0] / 255, color[1] / 255, color[2] / 255])
            self.saveSegment(new_pcd, surface_area, color)

            # Update the classified point cloud
            self.constructNewClassifiedPointCloud()
            self.parent.classifiedResultChanged()

            # Update the ids
            self.reassignSegmentIds()

    def saveSegment(self, pcd, surface_area, rgb):  
        print("saving...")      
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

    def deleteSegment(self, id):
        # Update CSV
        df = pd.read_csv("data/results/output.csv")
        df = df[df["Segment"] != id]
        df.to_csv("data/results/output.csv", index=False)

        # Delete PLY
        os.remove(f"data/planes/plane_{id}.ply")

    def constructNewClassifiedPointCloud(self):
        # Load in all point clouds
        pcds = []
        for file in os.listdir("data/planes"):
            if file.endswith(".ply"):
                pcd = o3d.io.read_point_cloud(f"data/planes/{file}")
                pcds.append(pcd)

        # Merge point clouds
        new_pcd = o3d.geometry.PointCloud()
        for pcd in pcds:
            new_pcd += pcd

        # Save point cloud
        o3d.io.write_point_cloud("data/results/result-classified.ply", new_pcd)

    def reassignSegmentIds(self):
        with open("data/results/output.csv", "r") as f:
            lines = f.readlines()[1:]

            # Temporarily rename all files
            for line in lines:
                print(f"data/planes/plane_{line.split(',')[0]}.ply")
                os.rename(f"data/planes/plane_{line.split(',')[0]}.ply", f"data/planes/plane_{line.split(',')[0]}_temp.ply")
            
            # Rename plane to new id
            for i, line in enumerate(lines):
                os.rename(f"data/planes/plane_{line.split(',')[0]}_temp.ply", f"data/planes/plane_{i + 1}.ply")

            f.close()

        # Update CSV
        df = pd.read_csv("data/results/output.csv")
        df["Segment"] = range(1, len(df) + 1)
        df.to_csv("data/results/output.csv", index=False)

        
        