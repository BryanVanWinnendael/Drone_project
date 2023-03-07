import sys
import open3d as o3d

def viewMesh(filename):
    mesh = o3d.io.read_triangle_mesh(filename)
    o3d.visualization.draw_geometries([mesh])

def viewPointCloud(filename):
    pcd = o3d.io.read_point_cloud(filename)
    o3d.visualization.draw_geometries([pcd])

def viewResult():
    filename = "data/results/result-classified.ply"
    viewPointCloud(filename)

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python viewData.py <mesh/point-cloud> <file>")
        exit(1)
    else:
        if sys.argv[1] == "mesh":
            viewMesh(sys.argv[2])
        elif sys.argv[1] == "point-cloud":
            viewPointCloud(sys.argv[2])
        else:
            print("Usage: python viewData.py <mesh/point-cloud> <file>")
            exit(1)