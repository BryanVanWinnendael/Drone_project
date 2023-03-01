import os
from PyQt5 import QtCore
import datetime
from model.clean import clean

clusterStrategies = ["DBSCAN", "None", "Agglomerative"]

defaultSettings = {
    "Cluster strategy": "None",
    "Minimum points": 30,
    "Iterations": 1000,
    "Maximum number of loops": 100,
    "Number of neigbours": 10,
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