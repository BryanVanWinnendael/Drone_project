import os
import pandas as pd
import open3d as o3d

def GetDefaulftParameters():
    return {
        "min_points": 100,
        "iterations": 1000,
        "max_loops": 100,
        "neighbours": 20,
        "voxel_size": 0.01,
        "treshold": 0.01,
        "min_std_ratio": 2.0,
        "min_ratio": 0.05,
        "epsilon": 0.1,
        "number_of_clusters": 3,
    }

def GetValidClusterStrategies():
    return ["DBSCAN", "Agglomerative"]

def reassignSegmentIds():
    with open("data/results/output.csv", "r") as f:
        lines = f.readlines()[1:]

        # Temporarily rename all files
        for line in lines:
            os.rename(f"data/planes/plane_{line.split(',')[0]}.ply", f"data/planes/plane_{line.split(',')[0]}_temp.ply")
        
        # Rename plane to new id
        for i, line in enumerate(lines):
            os.rename(f"data/planes/plane_{line.split(',')[0]}_temp.ply", f"data/planes/plane_{i + 1}.ply")

        f.close()

    # Update CSV
    df = pd.read_csv("data/results/output.csv")
    df["Segment"] = range(1, len(df) + 1)
    df.to_csv("data/results/output.csv", index=False)

def constructNewClassifiedPointCloud():
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

def deleteSegment(id):
    # Check if there are still planes left
    if len(os.listdir("data/planes")) > 1:
        # Update CSV
        df = pd.read_csv("data/results/output.csv")
        df = df[df["Segment"] != id]
        df.to_csv("data/results/output.csv", index=False)

        # Delete PLY
        if os.path.isfile(f"data/planes/plane_{id}.ply"):
            os.remove(f"data/planes/plane_{id}.ply")
    else:
        print("Error: cannot delete last segment")