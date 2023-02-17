# Point cloud segmentation

## Introduction

This repository contains methods for simple point cloud segmentation. It will discover plains on a point cloud. It also contains extra functions to visualize the results.

### Plane segmentation

The plane segmentation is easy to use through the main.py file. It is used as followed: <br>
<code>python main.py filename</code>

This will load the point cloud and segment it. Each of the planes will be stored in a new planes folder. These planes will then be further processed into meshes in order to calculate the surface area of each plane.

These surfaces will then be written to a csv file.

The csv file and the full segmented point cloud will be stored in the results folder.

### Data transformation

There is also support for mesh files. These mesh files will be transformed into point clouds and then the process above is repeated.

Usage of data transformation as follows: <br>
<code>
    python mesh_to_point_cloud.py filename
</code>

### Data visualization

You can also visualize your point clouds and meshes. This is done through the view_data.py file as follows: <br>
<code>
    python view_data.py mesh/point-cloud filename
</code>

### Clean up
There is also a cleanup function to remove the planes, meshes and result folder contents. You can choose if you want to remove the results folder by adding an extra parameter. Usage as follows:<br>
<code>
    python clean.py # Removes all planes and meshes
    python clean.py hard # Removes all planes, meshes and results 
</code>

#### Credits

The plane_detection code is based on the following repository, but has been modified for our purposes: <link>https://github.com/yuecideng/Multiple_Planes_Detection</link>