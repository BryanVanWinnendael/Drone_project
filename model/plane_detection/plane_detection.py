import json
import numpy as np
import open3d as o3d
import os
from model.plane_detection.color_generator import GenerateColors
import csv

def ReadPlyPoint(fname):
    pcd = o3d.io.read_point_cloud(fname)
    return PCDToNumpy(pcd)

def NumpyToPCD(xyz):
    pcd = o3d.geometry.PointCloud()
    pcd.points = o3d.utility.Vector3dVector(xyz)
    return pcd

def PCDToNumpy(pcd):
    return np.asarray(pcd.points)

def RemoveNan(points):
    return points[~np.isnan(points[:, 0])]

def RemoveNoiseStatistical(pc, nb_neighbors=20, std_ratio=2.0):
    pcd = NumpyToPCD(pc)
    cl, ind = pcd.remove_statistical_outlier(
        nb_neighbors=nb_neighbors, std_ratio=std_ratio)
    return PCDToNumpy(cl)

def DownSample(pts, voxel_size=0.003):
    p = NumpyToPCD(pts).voxel_down_sample(voxel_size=voxel_size)
    return PCDToNumpy(p)

def PlaneRegression(points, threshold=0.01, init_n=3, iter=1000):
    pcd = NumpyToPCD(points)
    w, index = pcd.segment_plane(
        threshold, init_n, iter)
    return w, index

def DrawResult(points, colors):
    pcd = o3d.geometry.PointCloud()
    pcd.points = o3d.utility.Vector3dVector(points)
    pcd.colors = o3d.utility.Vector3dVector(colors)
    o3d.visualization.draw_geometries([pcd])

def SaveResult(points, colors, filename):
    pcd = o3d.geometry.PointCloud()
    pcd.points = o3d.utility.Vector3dVector(points)
    pcd.colors = o3d.utility.Vector3dVector(colors)

    # Create directory to save results
    if not os.path.exists("data/results"):
                os.makedirs("data/results")

    o3d.io.write_point_cloud("data/results/result-classified.ply", pcd)
    recent_file = {
        "name": filename,
    }

    json_object = json.dumps(recent_file, indent=4)

    with open("data/results/recent-file.json", "w") as outfile:
        outfile.write(json_object)



def DetectMultiPlanes(points, min_ratio=0.05, threshold=0.01, iterations=1000):
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

    return plane_list

def GetColor(class_name):
    if class_name == "roof":
        return [0.7, 0, 0]
    elif class_name == "wall":
        return [0, 0.7, 0]
    elif class_name == "window":
        return [0, 0, 0.7]
    else:
        return [0, 0, 0]

def DetectPlanes(filename, waitingScreen):
    import random
    import time

    points = ReadPlyPoint(filename)

    # pre-processing
    print('Pre-processing the point cloud...')
    waitingScreen.progress.emit('Pre-processing the point cloud...')

    points = RemoveNan(points)
    points = DownSample(points,voxel_size=0.003)
    # points = RemoveNoiseStatistical(points, nb_neighbors=50, std_ratio=0.5)

    t0 = time.time()
    results = DetectMultiPlanes(points, min_ratio=0.05, threshold=0.005, iterations=2000)

    print('Done detection planes after: ', time.time() - t0, " seconds")

    planes = []
    generated_colors = GenerateColors(len(results))
    colors = []

    classes = ["roof", "wall", "window"]
    csv_planes = {}

    # Create directory to save planes
    if not os.path.exists("data/planes"):
        os.makedirs("data/planes")

    for i, (w, plane) in enumerate(results):
        # Grab a random class
        class_name = random.choice(classes)

        # r = generated_colors[i][0] / 255
        # g = generated_colors[i][1] / 255
        # b = generated_colors[i][2] / 255

        # Get color from class
        r, g, b = GetColor(class_name)

        color = np.zeros((plane.shape[0], plane.shape[1]))
        color[:, 0] = r
        color[:, 1] = g
        color[:, 2] = b

        colors.append(color)
        planes.append(plane)

        # Save plane to PLY file
        pcd = o3d.geometry.PointCloud()
        pcd.points = o3d.utility.Vector3dVector(plane)
        pcd.colors = o3d.utility.Vector3dVector(colors[i])

        o3d.io.write_point_cloud(f'data/planes/plane_{i + 1}.ply', pcd)

        csv_planes[i + 1] = class_name

    # Write class and segment to csv
    with open('data/results/planes.csv', mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Segment', 'Class', 'Surface area']) # Write header row
        for key, value in csv_planes.items():
            writer.writerow([key, value])

    planes = np.concatenate(planes, axis=0)
    colors = np.concatenate(colors, axis=0)

    print('Saving results...')
    waitingScreen.progress.emit('Saving results...')

    SaveResult(planes, colors, filename)