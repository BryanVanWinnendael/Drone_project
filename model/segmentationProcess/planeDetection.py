import numpy as np
import open3d as o3d

from sklearn.cluster import AgglomerativeClustering

from model.segmentationProcess.colorGenerator import GenerateColors
from model.utils import getDefaulftParameters, getValidClusterStrategies

def saveResult(planes):
    pcds = o3d.geometry.PointCloud()
    for plane in planes:
        pcds += plane

    o3d.io.write_point_cloud("data/results/result-classified.ply", pcds)

def findLargestCluster(points, labels):
    largest_cluster = 0
    largest_cluster_size = 0

    for label in np.unique(labels):
        cluster_size = len(points[labels == label])
        if cluster_size > largest_cluster_size:
            largest_cluster = label
            largest_cluster_size = cluster_size

    return largest_cluster

def segmentPlanes(pcd, cluster=None, parameters=getDefaulftParameters()):
    # Prepare necessary variables
    points = np.asarray(pcd.points)
    planes = []
    N = len(points)
    target = points.copy()
    count = 0
    max_loops = parameters["max_loops"]

    print(f"Starting with {N} points")

    # Because infinite loops are possible we limit the max amount of loops
    # Loop until the minimum ratio of points is reached, this will limit the amount of planes which results in less computation time
    # You can put min ratio to 0 to get all planes, but this will take a lot of time
    while count < (1 - parameters["min_ratio"]) * N and max_loops > 0:
        # Convert back to open3d point cloud
        cloud = o3d.geometry.PointCloud()
        cloud.points = o3d.utility.Vector3dVector(target)

        # Segment the plane
        inliers, mask = cloud.segment_plane(distance_threshold=parameters["treshold"], ransac_n=3, num_iterations=parameters["iterations"])

        # Extract the plane
        plane = cloud.select_by_index(mask)

        if cluster != None and cluster in getValidClusterStrategies():
            inlier_points = np.asarray(plane.points)
            redistributing = parameters["redistribute_smaller_clusters"]
  
            # Remaining clusters
            remaining_clusters = []

            if cluster == "DBSCAN":
                # Perform DBSCAN clustering on the points
                # The minimum number of points is set to 20, because if the parameter value is used it gives weird results
                labels = np.array(plane.cluster_dbscan(eps=parameters["epsilon"], min_points=20))
            elif cluster == "Agglomerative":
                # Perform agglomerative clustering on the points
                labels = AgglomerativeClustering(n_clusters=parameters["number_of_clusters"]).fit_predict(inlier_points)

            # Find the largest cluster
            largest_cluster = findLargestCluster(inlier_points, labels)
            
            # Extract points for each cluster
            for label in np.unique(labels):
                # Get the points for this cluster
                cluster_points = inlier_points[labels == label]

                correct_label = label == largest_cluster
                enough_points = len(cluster_points) >= parameters["min_points"]

                if (redistributing and correct_label and enough_points) or (not redistributing and enough_points):
                    # Convert points to Open3D point cloud
                    cluster_pcd = o3d.geometry.PointCloud()
                    cluster_pcd.points = o3d.utility.Vector3dVector(cluster_points)
                    # Add the cluster point cloud to the list of planes
                    planes.append(cluster_pcd)
                    # Update the count
                    count += len(cluster_points)
                else:
                    # Put the points back into the target
                    print("Not enough points to be a plane, adding points back to target")
                    remaining_clusters.append(cluster_points)
        else:
            # Add the plane to the list
            planes.append(plane)

            # Update the count
            count += len(mask)

        # Remove the plane from the target
        target = np.delete(target, mask, axis=0)

        # Add the remaining points back to the target
        if cluster != "None":
            for remaining_cluster in remaining_clusters:
                target = np.concatenate((target, remaining_cluster), axis=0)

        max_loops -= 1

    # Check if all loops were used and if so add the remaining points to a plane
    if max_loops <= 0 and len(target) >= parameters["min_points"]:
        print("Adding remaining points to a plane")
        plane = o3d.geometry.PointCloud()
        plane.points = o3d.utility.Vector3dVector(target)
        planes.append(plane)


    print(f"Found {len(planes)} planes")

    return planes

# Detect planes solely based on RANSAC
def detectPlanes(filename, waitingScreen, cluster=None, parameters=getDefaulftParameters()):
    # Load in point cloud
    print("Loading point cloud...")
    waitingScreen.progress.emit("Loading point cloud...")
    pcd = o3d.io.read_point_cloud(filename)

    # Preprocess the point cloud
    print("Preprocessing point cloud...")
    pcd = pcd.voxel_down_sample(voxel_size=parameters["voxel_size"])
    pcd, mask = pcd.remove_statistical_outlier(nb_neighbors=parameters["neighbours"], std_ratio=parameters["min_std_ratio"])
    # This was removed for now because it was causing the point cloud to be too small
    # pcd, mask = pcd.remove_radius_outlier(nb_points=16, radius=0.05)

    # Segment the planes
    print("Segmenting planes...")
    waitingScreen.progress.emit("Segmenting planes...")
    planes = segmentPlanes(pcd, cluster=cluster, parameters=parameters)

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
    saveResult(planes)