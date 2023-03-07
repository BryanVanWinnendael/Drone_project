import sys
import open3d as o3d

def convertMeshToPointCloud(filename):
    print("Reading point cloud from file: " + filename)
    mesh = o3d.io.read_triangle_mesh(filename)
    print("Converting mesh to point cloud by sampling...")
    pcd = mesh.sample_points_poisson_disk(16384)
    print("Succesfully sampled point cloud from mesh. Writing to file...")
    o3d.io.write_point_cloud("data/point_cloud.ply", pcd)
    print("Succesfully wrote point cloud to file.")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python mesh_to_point_cloud.py <file>")
        exit(1)
    else:
        filename = sys.argv[1]
        convertMeshToPointCloud(filename)