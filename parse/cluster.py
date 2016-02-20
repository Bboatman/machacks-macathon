import re
from numpy import array
from scipy.cluster.vq import vq, kmeans2, whiten
import LatLon

jsonEvents = open("jsonEvents.txt", "r")
class NewsEvent():
    
    def __init__(self):
        self.gps = ""
        self.url = ""
        self.lat = ""
        self.lon = ""
    
    def setUrl(self,val):
        self.url = str(val)
        
    def setGps(self, val):
        self.gps = str(val)
    
    def setlon(self, val):
        self.lon = str(val)

    def setlat(self, val):
        self.lat = str(val)

    def getUrl(self):
        return str(self.url)
        
    def getGps(self):
        return str(self.gps)
        
    def getlon(self):
        return str(self.lon)

    def getlat(self):
        return str(self.lat)

        
    def __str__(self):
        return "{\"lat\": " + self.getlat() + ", \"lon\": " + self.getlon() + ", \"url\": \"" + self.getUrl() + "\"}"
        
def readInEvents():
    events = []
    for line in jsonEvents:
        dataArr = line.split(": ")
        e = NewsEvent()
        e.setGps(dataArr[1][0:-5])
        e.setUrl(dataArr[2][0:-1])
        coordArr = e.getGps().split(", ")
        print(coordArr)
        coordArr[0] = coordArr[0].replace('m','').replace('s','')
        coordArr[1] = coordArr[1].replace('m','').replace('s','')
        x = coordArr[0]
        y = coordArr[1]
        print(type(LatLon.string2latlon(x, y, 'd% %m% %S% %H' )))

        lat, lon = LatLon.string2latlon(x, y, 'd% %m% %S% %H' ).to_string()
        e.setlat(lat)
        e.setlon(lon)

        events.append(e)
    return events

def generateClusters():
    events = readInEvents()
    features = []
    for e in events:
        print("latitude: "+ e.getlat())
        print("longitude: "+ e.getlon())
        features.append([float(e.getlat()), float(e.getlon())])
    features = array(features)
    centroids, indices = kmeans2(whiten(features), 3, iter = 20) 
    return centroids, indices, events
    

def clusterToJson(centroids, indices, events):
    masterStr = "["
    cumulativeSize = 0
    for i in range(len(centroids)):    
        clusterStr = "{\"events\":["
        size = 0
        for j in range(len(indices)):
            size += 1
            clusterStr += str(events[j]) + ","
        if j == len(indices) -1:
            clusterStr = clusterStr[0:-1]
            clusterStr += "],"
        cumulativeSize += size
        clusterStr += "\"size\": " + str(size)
        clusterStr += ",\"center\":{ \"lat\":" + str(centroids[i][0]) + ",\"lon\":" + str(centroids[i][1]) + "}},"
        masterStr += clusterStr
        if i == len(centroids) - 1:
            masterStr = masterStr[0:-1]
    masterStr += "]"
    return masterStr
        
            
centroids, indices, events = generateClusters()
jsonFile = open("jsonClusters.txt", "w")
jsonFile.write(clusterToJson(centroids, indices, events))