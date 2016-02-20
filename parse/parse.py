from keywordFinder import getArticles
from geopy import geolocator

states = ["Alabama", "Alaska","Arizona","Arkansas","California","Colorado","Connecticut","Delaware","Florida","Georgia","Hawaii","Idaho","Illinois","Indiana","Iowa","Kansas","Kentucky","Louisiana","Maine","Maryland","Massachusetts","Michigan","Minnesota","Mississippi","Missouri","Montana","Nebraska","Nevada","New Hampshire","New Jersey","New Mexico","New York","North Carolina","North Dakota","Ohio","Oklahoma","Oregon","Pennsylvania","Rhode Island","South Carolina","South Dakota","Tennessee","Texas","Utah","Vermont","Virginia","Washington","West Virginia","Wisconsin","Wyoming"]
properNouns = []
index = 0
for article in getArticles():
    for line in article:
        wordArray = line.split(" ")
        for word in wordArray:
            if len(word) > 1:
                if word[0].isupper():
                    wordTuple = (word, index)
                    if wordTuple not in properNouns:
                        properNouns.append((word,index))
    index += 1
    
geolocator = geolocator.Nominatim()

for item in properNouns:
    if (item[0] in states) or (item[0][0:-1] in states):
        print(item)
        location = geolocator.geocode(item[0])
        print(location.address)