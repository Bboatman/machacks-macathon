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
        return "{""coordinates"": " + self.getGps() + ", ""url"": " + self.getUrl() + "}"
        
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

        print(e.getlat())
        print(e.getlon())
        events.append(e)
    return events

# def degree2dec(dms_str):
#     dms_str = re.sub(r'\s', '', dms_str)
#     if re.search('[swSW]', dms_str):
#         sign = -1
#     else:
#         sign = 1

#     (degree, minute, second, frac_seconds) = re.split('\D+', dms_str, maxsplit=4)
#     second += "." + frac_seconds
#     return sign * (int(degree) + float(minute) / 60 + float(second) / 3600)
    
# def conversion(old):
#     direction = {'N':-1, 'S':1, 'E': -1, 'W':1}
#     new = old.replace('m',' ').replace(' ',' ').replace('s',' ')
#     new = new.split(", ")
#     new_dir = new.pop()
#     new.extend([0,0,0])
#     return (int(new[0])+int(new[1])/60.0+int(new[2])/3600.0) * direction[new_dir]

events = readInEvents()
features = []
for e in events:
    print("latitude: "+ e.getlat())
    print("longitude: "+ e.getlon())
    features.append([float(e.getlat()), float(e.getlon())])
features = array(features)
x, y = kmeans2(whiten(features), 3, iter = 20) 
#kmeans2(features,2)
