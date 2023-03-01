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