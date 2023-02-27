import open3d as o3d
import sys

def ViewMesh(filename):
    mesh = o3d.io.read_triangle_mesh(filename)
    o3d.visualization.draw_geometries([mesh])

def ViewPointCloud(filename):
    pcd = o3d.io.read_point_cloud(filename)
    o3d.visualization.draw_geometries([pcd])

def ViewResult():
    filename = "data/results/result-classified.ply"
    ViewPointCloud(filename)

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python view_data.py <mesh/point-cloud> <file>")
        exit(1)
    else:
        if sys.argv[1] == "mesh":
            ViewMesh(sys.argv[2])
        elif sys.argv[1] == "point-cloud":
            ViewPointCloud(sys.argv[2])
        else:
            print("Usage: python view_data.py <mesh/point-cloud> <file>")
            exit(1)