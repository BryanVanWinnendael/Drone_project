import json
from PyQt5 import QtCore
import datetime
from model.clean import clean

defaultSettings = {
    "Treshhold": 0.5,
    "Number of neigbours": 10,
    "Radius": 0.5,
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

    if savedsettings.value("settings") == None:
        saveSettings(defaultSettings)
    
    return savedsettings.value("settings")

def resetSettings():
    saveSettings(defaultSettings)
    return defaultSettings

def cleanData(hard=False):
    clean(hard=hard)

def updateClass(row, col, newItem):
    if col != 1: return
    row += 1
    res_path = "data/results/output.csv"
    with open(res_path, "r") as infile:
        data = infile.read()
        data = data.split("\n")
        data[row] = data[row].split(",")
        data[row][col] = newItem
        data[row] = ",".join(data[row])
        data = "\n".join(data)

    with open(res_path, "w") as outfile:
        outfile.write(data)