import open3d as o3d
from model.plane_detection.color_generator import GenerateColors
import numpy as np
from sklearn.cluster import DBSCAN

def SaveResult(planes):
    pcds = o3d.geometry.PointCloud()
    for plane in planes:
        pcds += plane

    o3d.io.write_point_cloud("data/results/result-classified.ply", pcds)

def SegmentPlanes(pcd, waitingScreen, min_ratio=0.05, threshold=0.01, iterations=1000):
    points = np.asarray(pcd.points)
    plane_list = []
    N = len(points)
    target = points.copy()
    count = 0

    while count < (1 - min_ratio) * N:
        cloud = o3d.geometry.PointCloud()
        cloud.points = o3d.utility.Vector3dVector(target)

        inliers, mask = cloud.segment_plane(distance_threshold=threshold, ransac_n=3, num_iterations=iterations)
    
        count += len(mask)

        # Extract the plane
        plane = cloud.select_by_index(mask)

        plane_list.append(plane)
        target = np.delete(target, mask, axis=0)

    print("Found {} planes".format(len(plane_list)))

    return plane_list

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
    # pcd, mask = pcd.remove_radius_outlier(nb_points=16, radius=0.05)
    print("Ending with {} points".format(len(pcd.points)))
    pcd.estimate_normals(search_param=o3d.geometry.KDTreeSearchParamHybrid(radius=0.1, max_nn=30))


    # Segment the planes
    print("Segmenting planes...")
    waitingScreen.progress.emit("Segmenting planes...")
    planes = SegmentPlanes(pcd, waitingScreen)

    # while len(pcd.points) >= minimum_number:
    #     # Use RANSAC to segment the plane
    #     # 4 points are needed for convex hull
    #     plane_model, inliers = pcd.segment_plane(distance_threshold=0.01, ransac_n=3, num_iterations=2000)

    #     # Extract the inlier points
    #     inlier_cloud = pcd.select_by_index(inliers)

    #     # Extract inlier points
    #     inlier_points = np.asarray(pcd.points)[inliers, :]

    #     # Perform DBSCAN clustering on inlier points
    #     clustering = DBSCAN(eps=0.05, min_samples=10).fit(inlier_points)

    #     # Identify main plane cluster by finding largest cluster
    #     labels = clustering.labels_
    #     unique_labels, counts = np.unique(labels, return_counts=True)
    #     main_label = unique_labels[np.argmax(counts)]

    #     if (len(unique_labels) > 1):
    #         print("More than one plane detected")

    #     # Extract points in main plane cluster
    #     main_cluster_points = inlier_points[labels == main_label]

    #     # Convert points to Open3D point cloud
    #     plane = o3d.geometry.PointCloud()
    #     plane.points = o3d.utility.Vector3dVector(main_cluster_points)

    #     # Extract the outlier points
    #     pcd = pcd.select_by_index(inliers, invert=True)

    #     # Add the plane to the list of planes
    #     planes.append(plane)

    # for plane in planes:
    #     if len(plane.points) < 4:
    #         planes.remove(plane)

    # Generate random colors for each plane
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