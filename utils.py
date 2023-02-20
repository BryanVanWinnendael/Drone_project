import json
from PyQt5 import QtCore
import datetime
import os
import sys

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

def getRecentFile():
    try :
        with open('data/results/recent-file.json', 'r') as openfile:
            json_object = json.load(openfile)
    except:
        return None
 
    return json_object.get("name")

def clean(hard=False):
    if os.path.exists("data/planes"):
        for filename in os.listdir('data/planes'):
            os.remove("data/planes/" + filename)
    if os.path.exists("data/meshes"):
        for filename in os.listdir('data/meshes'):
            os.remove("data/meshes/" + filename)
    if hard and os.path.exists("data/results"):
        for filename in os.listdir('data/results'):
            os.remove("data/results/" + filename)