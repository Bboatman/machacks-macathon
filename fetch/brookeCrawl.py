from html.parser import HTMLParser  
from urllib.request import urlopen  
from urllib import parse

year = "2016"

class LinkParser(HTMLParser):
    def __init__(self):
        global dataIndices 
        dataIndices = []
        HTMLParser.__init__(self)
        
    def getIndices(self):
        return dataIndices
        
    def handle_starttag(self, tag, attrs):
        # We are looking for the begining of a link. Links normally look
        # like <a href="www.someurl.com"></a>
        if tag  == 'a':
            for (key, value) in attrs:
                if key == 'href':
                    if year in value:
                        newUrl = parse.urljoin(self.baseUrl, value)
                    # And add it to our colection of links:
                        self.links = self.links + [newUrl]
        if tag == "p":
            check = attrs[0][1]
            if check == 'zn-body__paragraph':
                dataIndices.append(self.getpos()[1])


    def getLinks(self, url):
        self.links = []
        self.data = []
        self.baseUrl = url
        response = urlopen(url)
        if response.getheader('Content-Type')=='text/html; charset=utf-8':
            htmlBytes = response.read()
            htmlString = htmlBytes.decode("utf-8")
            self.feed(htmlString)
            return htmlString, self.links
        else:
            print("Done fucked up")
            return "",[]

def newsCrawler(url, wordBank, maxPages):  
    pagesToVisit = [url]
    numberVisited = 0
    while numberVisited < maxPages and pagesToVisit != []:
        numberVisited = numberVisited +1
        # Start from the beginning of our collection of pages to visit:
        url = pagesToVisit[0]
        pagesToVisit = pagesToVisit[1:]
        try:
            print(numberVisited, "Visiting:", url)
            parser = LinkParser()
            data, links = parser.getLinks(url) #links should only be links to articles
            for index in parser.getIndices():
                print(data[index+30:data.find("</p>", index)])
            for word in wordBank: 
                wordScore = data.find(word)
                pagesToVisit = pagesToVisit + links
                print(" **Found:**", word, " ", wordScore," times")
        except(e):
            print(e)

def getWordBank(pathToWordBank):
    wordBankFile = open(pathToWordBank, 'r')
    wordBank = []
    
    for line in wordBankFile:
        line = line.strip('\n')
        wordBank.append(line)
    
    return wordBank

newsCrawler("http://www.cnn.com/2016/02/18/world/uganda-election-social-media-shutdown/index.html", [''], 1)