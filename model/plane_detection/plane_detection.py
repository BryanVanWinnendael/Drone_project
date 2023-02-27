import open3d as o3d
from model.plane_detection.color_generator import GenerateColors
import numpy as np
from sklearn.cluster import DBSCAN

def SaveResult(planes):
    pcds = o3d.geometry.PointCloud()
    for plane in planes:
        pcds += plane

    o3d.io.write_point_cloud("data/results/result-classified.ply", pcds)

def SegmentPlanes(pcd, waitingScreen, min_ratio=0.05, threshold=0.01, iterations=1000, cluster=False):
    # Prepare necessary variables
    points = np.asarray(pcd.points)
    planes = []
    N = len(points)
    target = points.copy()
    count = 0

    # Loop until the minimum ratio of points is reached
    while count < (1 - min_ratio) * N:
        # Convert back to open3d point cloud
        cloud = o3d.geometry.PointCloud()
        cloud.points = o3d.utility.Vector3dVector(target)

        # Segment the plane
        inliers, mask = cloud.segment_plane(distance_threshold=threshold, ransac_n=3, num_iterations=iterations)
    
        # Update the count
        count += len(mask)

        # Extract the plane
        plane = cloud.select_by_index(mask)

        if cluster:
            inlier_points = np.asarray(plane.points)

            # Perform DBSCAN clustering on the points
            labels = np.array(plane.cluster_dbscan(eps=0.1, min_points=20, print_progress=True))

            # Extract points for each cluster
            for label in np.unique(labels):
                # Get the points for this cluster
                cluster_points = inlier_points[labels == label]

                print("Found cluster with {} points".format(len(cluster_points)))

                if len(cluster_points) >= 200:
                    # Convert points to Open3D point cloud
                    cluster_pcd = o3d.geometry.PointCloud()
                    cluster_pcd.points = o3d.utility.Vector3dVector(cluster_points)

                    # Add the cluster point cloud to the list of planes
                    planes.append(cluster_pcd)
        else:
            # Add the plane to the list
            planes.append(plane)

        # Remove the plane from the target
        target = np.delete(target, mask, axis=0)

    print("Found {} planes".format(len(planes)))

    return planes

# Detect planes solely based on RANSAC
def DetectPlanes(filename, minimum_number, waitingScreen):
    # Load in point cloud
    print("Loading point cloud...")
    waitingScreen.progress.emit("Loading point cloud...")
    pcd = o3d.io.read_point_cloud(filename)

    # Preprocess the point cloud
    print("Preprocessing point cloud...")
    print("Starting with {} points".format(len(pcd.points)))
    pcd = pcd.voxel_down_sample(voxel_size=0.01)
    pcd, mask = pcd.remove_statistical_outlier(nb_neighbors=5, std_ratio=2.0)
    # This was removed for now because it was causing the point cloud to be too small
    # pcd, mask = pcd.remove_radius_outlier(nb_points=16, radius=0.05)
    print("Ending with {} points".format(len(pcd.points)))
    pcd.estimate_normals(search_param=o3d.geometry.KDTreeSearchParamHybrid(radius=0.1, max_nn=30))


    # Segment the planes
    print("Segmenting planes...")
    waitingScreen.progress.emit("Segmenting planes...")
    planes = SegmentPlanes(pcd, waitingScreen, cluster=True)

    # Generate range of colors
    colors = GenerateColors(len(planes))

    print("Planes detected: " + str(len(planes)))
    waitingScreen.progress.emit("Planes detected: " + str(len(planes)))

    # Loop through each plane and save it to a file
    print("Saving planes...")
    waitingScreen.progress.emit("Saving planes...")
    for i, plane in enumerate(planes):
        r = colors[i][0] / 255
        g = colors[i][1] / 255
        b = colors[i][2] / 255

        plane.paint_uniform_color([r, g, b])
        o3d.io.write_point_cloud("data/planes/plane_" + str(i + 1) + ".ply", plane)
    
    # Save the result
    print("Saving result...")
    waitingScreen.progress.emit("Saving result...")
    SaveResult(planes)