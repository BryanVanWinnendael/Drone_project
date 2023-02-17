import numpy as np
import open3d as o3d
import os
from model.plane_detection.color_generator import GenerateColors

def ReadPlyPoint(fname):
    """ read point from ply
    Args:
        fname (str): path to ply file
    Returns:
        [ndarray]: N x 3 point clouds
    """

    pcd = o3d.io.read_point_cloud(fname)

    return PCDToNumpy(pcd)


def NumpyToPCD(xyz):
    """ convert numpy ndarray to open3D point cloud 
    Args:
        xyz (ndarray): 
    Returns:
        [open3d.geometry.PointCloud]: 
    """

    pcd = o3d.geometry.PointCloud()
    pcd.points = o3d.utility.Vector3dVector(xyz)

    return pcd


def PCDToNumpy(pcd):
    """  convert open3D point cloud to numpy ndarray
    Args:
        pcd (open3d.geometry.PointCloud): 
    Returns:
        [ndarray]: 
    """

    return np.asarray(pcd.points)


def RemoveNan(points):
    """ remove nan value of point clouds
    Args:
        points (ndarray): N x 3 point clouds
    Returns:
        [ndarray]: N x 3 point clouds
    """

    return points[~np.isnan(points[:, 0])]


def RemoveNoiseStatistical(pc, nb_neighbors=20, std_ratio=2.0):
    """ remove point clouds noise using statitical noise removal method
    Args:
        pc (ndarray): N x 3 point clouds
        nb_neighbors (int, optional): Defaults to 20.
        std_ratio (float, optional): Defaults to 2.0.
    Returns:
        [ndarray]: N x 3 point clouds
    """

    pcd = NumpyToPCD(pc)
    cl, ind = pcd.remove_statistical_outlier(
        nb_neighbors=nb_neighbors, std_ratio=std_ratio)

    return PCDToNumpy(cl)


def DownSample(pts, voxel_size=0.003):
    """ down sample the point clouds
    Args:
        pts (ndarray): N x 3 input point clouds
        voxel_size (float, optional): voxel size. Defaults to 0.003.
    Returns:
        [ndarray]: 
    """

    p = NumpyToPCD(pts).voxel_down_sample(voxel_size=voxel_size)

    return PCDToNumpy(p)


def PlaneRegression(points, threshold=0.01, init_n=3, iter=1000):
    """ plane regression using ransac
    Args:
        points (ndarray): N x3 point clouds
        threshold (float, optional): distance threshold. Defaults to 0.003.
        init_n (int, optional): Number of initial points to be considered inliers in each iteration
        iter (int, optional): number of iteration. Defaults to 1000.
    Returns:
        [ndarray, List]: 4 x 1 plane equation weights, List of plane point index
    """

    pcd = NumpyToPCD(points)

    w, index = pcd.segment_plane(
        threshold, init_n, iter)

    return w, index


def DrawResult(points, colors):
    pcd = o3d.geometry.PointCloud()
    pcd.points = o3d.utility.Vector3dVector(points)
    pcd.colors = o3d.utility.Vector3dVector(colors)
    o3d.visualization.draw_geometries([pcd])

def SaveResult(points, colors):
    pcd = o3d.geometry.PointCloud()
    pcd.points = o3d.utility.Vector3dVector(points)
    pcd.colors = o3d.utility.Vector3dVector(colors)

    if not os.path.exists("data/results"):
                os.makedirs("data/results")

    o3d.io.write_point_cloud("data/results/result-classified.ply", pcd)

def DetectMultiPlanes(points, min_ratio=0.05, threshold=0.01, iterations=1000):
    """ Detect multiple planes from given point clouds
    Args:
        points (np.ndarray): 
        min_ratio (float, optional): The minimum left points ratio to end the Detection. Defaults to 0.05.
        threshold (float, optional): RANSAC threshold in (m). Defaults to 0.01.
    Returns:
        [List[tuple(np.ndarray, List)]]: Plane equationand plane point index
    """

    plane_list = []
    N = len(points)
    target = points.copy()
    count = 0

    while count < (1 - min_ratio) * N:
        w, index = PlaneRegression(
            target, threshold=threshold, init_n=3, iter=iterations)
    
        count += len(index)
        plane_points = target[index]
        plane_list.append((w, target[index]))
        target = np.delete(target, index, axis=0)

        # Save plane to PLY file
        if not os.path.exists("data/planes"):
            os.makedirs("data/planes")

        pcd = NumpyToPCD(plane_points)
        o3d.io.write_point_cloud(f'data/planes/plane_{len(plane_list)}.ply', pcd)

    return plane_list


def DetectPlanes(filename):
    import random
    import time

    points = ReadPlyPoint(filename)

    # pre-processing
    print('Pre-processing the point cloud...')
    points = RemoveNan(points)
    points = DownSample(points,voxel_size=0.003)
    # points = RemoveNoiseStatistical(points, nb_neighbors=50, std_ratio=0.5)

    t0 = time.time()
    results = DetectMultiPlanes(points, min_ratio=0.05, threshold=0.005, iterations=2000)
    print('Done detection planes after: ', time.time() - t0, " seconds")
    planes = []
    generated_colors = GenerateColors(len(results))
    colors = []

    for i, (w, plane) in enumerate(results):
        r = generated_colors[i][0] / 255
        g = generated_colors[i][1] / 255
        b = generated_colors[i][2] / 255

        color = np.zeros((plane.shape[0], plane.shape[1]))
        color[:, 0] = r
        color[:, 1] = g
        color[:, 2] = b

        colors.append(color)
        planes.append(plane)

    planes = np.concatenate(planes, axis=0)
    colors = np.concatenate(colors, axis=0)

    print('Saving results...')
    SaveResult(planes, colors)