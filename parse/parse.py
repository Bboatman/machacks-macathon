from keywordFinder import getArticles
from geopy.geocoders import Nominatim
import itertools

'''
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
THIS ONLY RUNS IN PYTHON 2.x BECAUSE GEOPY IS ANCIENT
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
'''

geolocator = Nominatim()
articles = getArticles()
states = ["Alabama", "Alaska","Arizona","Arkansas","California","Colorado","Connecticut","Delaware","Florida","Georgia","Hawaii","Idaho","Illinois","Indiana","Iowa","Kansas","Kentucky","Louisiana","Maine","Maryland","Massachusetts","Michigan","Minnesota","Mississippi","Missouri","Montana","Nebraska","Nevada","New Hampshire","New Jersey","New Mexico","New York","North Carolina","North Dakota","Ohio","Oklahoma","Oregon","Pennsylvania","Rhode Island","South Carolina","South Dakota","Tennessee","Texas","Utah","Vermont","Virginia","Washington","West Virginia","Wisconsin","Wyoming"]
ignore = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday","Sunday"]
    

class NewsEvent():
    
    def __init__(self):
        self.eventstate = ""
        self.eventcity = ""
        self.gps = ""
    
    def setState(self,state):
        self.eventstate = str(state)
        
    def setCity(self,city):
        self.eventcity = str(city)
        
    def setGps(self, val):
        self.gps = str(val)
    
    def getCity(self):
        return str(self.eventcity)
    
    def getState(self):
        return str(self.eventstate)
        
    def getGps(self):
        return str(self.gps)
        
    def __str__(self):
        return self.getCity()+ " " + self.getState() +"\n" + self.getGps()
        
def getNouns():
    properNouns = []
    for i in range(len(articles)):
        properNouns.append([])
    index = 0
    for article in articles:
        for line in article:
            wordArray = line.split(" ")
            for word in wordArray:
                if len(word) > 1:
                    if word[0].isupper():
                        wordTuple = (word, index)
                        if wordTuple not in properNouns:
                            properNouns[index].append((word,index))
        index += 1
    return properNouns
    
def findLocs(properNouns):
    locs = []
    for i in range(len(articles)):
        locs.append(NewsEvent())
    
    for i in range(len(articles)): 
        for item in properNouns[i]:
            try:
                if (item[0] in states):
                    locs[i].setState(str(item[0]))
                if (item[0][0:-1] in states):
                    locs[i].setState(str(item[0][0:-1]))
            except :
                pass
    
    
    for i in range(len(locs)):
        loc = locs[i]
        if loc.getState() is not "":
            for item in properNouns[i]:
                try:
                    location = geolocator.geocode(item[0])
                    nameArr = str(location).split(", ")
                    if locs[i].getState() in nameArr:
                        if nameArr[0] not in ignore and nameArr[0] is not locs[i].getState():
                            print(nameArr)
                            locs[i].setCity(nameArr[0])
                            locs[i].setGps(location.point)
                            print location.point
                            break
                    if item[1] is not i:
                        break
                except:
                    pass
    return locs


def getCoordinates():
    urlData = open("jsonData.txt", "a")
    nouns = getNouns()
    locs = findLocs(nouns)
    for item in locs:
        val = str(item.getGps())
        txt = "dummy.url"
        jsonString = "{""coordinates"": " + val + ", ""url"": " + txt + "}"
        urlData.write(jsonString)


getCoordinates()
