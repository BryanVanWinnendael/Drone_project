import json
from PyQt5 import QtCore
import datetime
import os
from PyQt5.QtNetwork import QNetworkAccessManager, QNetworkRequest, QNetworkReply
from PyQt5.QtCore import QUrl

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

def cleanData(hard=False):
    if os.path.exists("data/planes"):
        for filename in os.listdir('data/planes'):
            os.remove("data/planes/" + filename)
    if os.path.exists("data/meshes"):
        for filename in os.listdir('data/meshes'):
            os.remove("data/meshes/" + filename)
    if hard and os.path.exists("data/results"):
        for filename in os.listdir('data/results'):
            os.remove("data/results/" + filename)

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

def doRequest(self):   
    url = "https://names.drycodes.com/10"
    req = QNetworkRequest(QUrl(url))
    
    self.nam = QNetworkAccessManager()
    self.nam.finished.connect(self.handleResponse)
    self.nam.get(req)

def handleResponse(self, reply):
    er = reply.error()
    if er == QNetworkReply.NoError:
        bytes_string = reply.readAll()
        print(str(bytes_string, 'utf-8'))
    else:
        print("Error occured: ", er)
        print(reply.errorString())