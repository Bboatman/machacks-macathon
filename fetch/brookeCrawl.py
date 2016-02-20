from html.parser import HTMLParser  
from urllib.request import urlopen  
from urllib import parse
from time import sleep

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
                    if ("2016" in value or "2015" in value or "2014" in value) and "video" not in value:
                        newUrl = parse.urljoin(self.baseUrl, value)
                    # And add it to our colection of links:
                        self.links = self.links + [newUrl]
        if tag == "p":
            check = "" 
            if len(attrs) > 0 and len(attrs[0]) > 1:
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
    pagesToVisit = url
    numberVisited = 0
    text = ""
    compoundScore = 0
    fileCount = 0
    count = 0
    
    while numberVisited < maxPages and pagesToVisit != []:
        text = ""
        numberVisited = numberVisited +1
        if numberVisited % 100 == 0:
            sleep(10)
        # Start from the beginning of our collection of pages to visit:
        url = pagesToVisit[0]
        pagesToVisit = pagesToVisit[1:]
        
        print(numberVisited, "Visiting:", url)
        parser = LinkParser()
        data, links = parser.getLinks(url)
        for index in parser.getIndices():
            endex = data.find("</p>", index)
            if len(data[index:endex]) < 1000:
                text = text + data[index+30:endex]
        pageScore = pageScorer(wordBank, text)
        if pageScore > len(wordBank) / 2:
            newfile = open("interestingArticles/" + str(count) + ".txt", 'w')
            newfile.write(url + " \n " + text)
            fileCount += 1
        pagesToVisit = pagesToVisit + links

def getWordBank(pathToWordBank):
    wordBankFile = open(pathToWordBank, 'r')
    wordBank = []
    
    for line in wordBankFile:
        line = line.strip('\n')
        wordBank.append(line)
    return wordBank

def pageScorer(wordBank, pageText):
    score = 0
    if len(pageText) > 0:
        keyWords = set(wordBank)
        textWords = set()
        for word in wordBank: 
            if word in pageText:
                textWords.add(word)
        intersection = keyWords & textWords
        if len(intersection) > len(wordBank) / 2:
            adjustedWordScore = len(intersection)**2
            score += adjustedWordScore
    print("Scored:", score)
    return score

newsCrawler(["http://www.cnn.com/specials/us/crime-and-justice", "http://www.cnn.com/2015/12/21/us/sandra-bland-no-indictments/", "http://www.cnn.com/2014/08/11/us/missouri-ferguson-michael-brown-what-we-know/", "http://www.cnn.com/2015/11/21/us/minneapolis-jamar-clark-police-shooting/", "http://www.cnn.com/2015/12/28/us/tamir-rice-shooting/"], getWordBank("../parse/wordbank.txt"), 500)
