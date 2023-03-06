import os
from PyQt5 import QtCore
import datetime
from model.clean import clean
from zipfile import ZipFile

clusterStrategies = ["DBSCAN", "None", "Agglomerative"]
surfaceStrategies = ["Poisson", "Convex Hull", "Ball Pivoting"]

defaultSettings = {
    "Cluster strategy": "None",
    "Surface strategy": "Convex Hull",
    "Redistribute smaller clusters": False,
    "Estimated planes": 0,
    "Minimum points": 30,
    "Iterations": 1000,
    "Maximum number of loops": 100,
    "Number of neighbours": 10,
    "Voxel size": 0.01,
    "Treshold": 0.01,
    "Standard deviation ratio": 2.0,
    "Minimum ratio": 0.05,
    "Epsilon (DBSCAN)": 0.1,
    "Number of Clusters (Agglomerative)": 3,
}

def saveFileName(fileName):
    savedFileNames = getFileNames()
    current_time = datetime.datetime.now()
    file = {"name": fileName, "time": current_time.strftime("%d/%m/%Y %H:%M")}

    if savedFileNames == None:
        savedFileNames = [file]
    else:
        if len(savedFileNames) == 5:
            savedFileNames.pop(-1)
            savedFileNames.insert(0, file)
        else:
            savedFileNames.insert(0, file)

    newSavedFileNames = QtCore.QSettings("Drone-app", "savedFileNames")
    newSavedFileNames.setValue("savedFileNames", savedFileNames)

def getFileNames():
    savedFileNames = QtCore.QSettings("Drone-app", "savedFileNames")
    return savedFileNames.value("savedFileNames")

def saveRecentFile(fileName):
    recentFile = QtCore.QSettings("Drone-app", "recentFile")
    recentFile.setValue("recentFile", fileName)

def getRecentFile():
    isdir = os.path.isdir("data/results")
    if not isdir: return None
    try :
        recentFile = QtCore.QSettings("Drone-app", "recentFile")
    except:
        return None
 
    return recentFile.value("recentFile")

def saveSettings(settings):
    savedsettings = QtCore.QSettings("Drone-app", "settings")
    savedsettings.setValue("settings", settings)

def getSettings():
    savedsettings = QtCore.QSettings("Drone-app", "settings")

    for key in defaultSettings.keys():
        if key not in savedsettings.value("settings").keys():
            saveSettings(defaultSettings)
            return defaultSettings

    if savedsettings.value("settings") == None:
        saveSettings(defaultSettings)
    
    return savedsettings.value("settings")

def resetSettings():
    saveSettings(defaultSettings)
    return defaultSettings

def cleanData(hard=False):
    clean(hard=hard)

def updateClass(row, col, newItem):
    if col != 2: return
    row += 1
    res_path = "data/results/output.csv"
    with open(res_path, "r") as infile:
        data = infile.read()
        data = data.split("\n")
        data[row] = data[row].split(",")
        data[row][col - 1] = newItem
        data[row] = ",".join(data[row])
        data = "\n".join(data)

    with open(res_path, "w") as outfile:
        outfile.write(data)

import shutil

def copyDirectory(src, dest):
    try:
        shutil.copytree(src, dest)
        print("Directory copied successfully")
    except shutil.Error as e:
        print(f"Error copying directory: {e}")
    except OSError as e:
        print(f"Error copying directory: {e}")

def checkDataDirectory(directory):
    if os.path.isdir(directory):
        contents = os.listdir(directory)
        
        # Check if the correct folders exist
        if "planes" in contents and "results" in contents:
            # Check if the results folder contains the correct files
            results = os.listdir(os.path.join(directory, "results"))
            if "original.ply" in results and "result-classified.ply" in results and "output.csv" in results:
                return True
            
    return False
    
def checkZippedData(filename):
    # Check if file exist
    if os.path.isfile(filename):
        # Check if file is a zip file
        if filename.endswith(".zip"):
            # Check if the zip file contains the correct folders
            with ZipFile(filename, "r") as zip_ref:
                contents = zip_ref.namelist()
                if "results/original.ply" in contents and "results/result-classified.ply" in contents and "results/output.csv" in contents:
                    return True
    return False
    
def copyZip(filename, destination):
    if os.path.isfile(filename):
        if filename.endswith(".zip"):
            with ZipFile(filename, "r") as zip_ref:
                zip_ref.extractall(destination)