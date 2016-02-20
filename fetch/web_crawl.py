from html.parser import HTMLParser  
from urllib.request import urlopen  
from urllib import parse

year = "2016"

# We are going to create a class called LinkParser that inherits some
# methods from HTMLParser which is why it is passed into the definition
# from:git http://www.netinstructions.com/how-to-make-a-web-crawler-in-under-50-lines-of-python-code/
class LinkParser(HTMLParser):

    # This is a function that HTMLParser normally has
    # but we are adding some functionality to it
    def handle_starttag(self, tag, attrs):
        # We are looking for the begining of a link. Links normally look
        # like <a href="www.someurl.com"></a>
        if tag  == 'a':
            for (key, value) in attrs:
                if key == 'href':
                    # We are grabbing the new URL. We are also adding the
                    # base URL to it. For example:
                    # www.netinstructions.com is the base and
                    # somepage.html is the new URL (a relative URL)
                    #
                    # We combine a relative URL with the base URL to create
                    # an absolute URL like:
                    # www.netinstructions.com/somepage.html
                    if year in value:
                        newUrl = parse.urljoin(self.baseUrl, value)
                    # And add it to our colection of links:
                        self.links = self.links + [newUrl]

    # This is a new function that we are creating to get links
    # that our spider() function will call
    def getLinks(self, url):
        self.links = []
        # Remember the base URL which will be important when creating
        # absolute URLs
        self.baseUrl = url
        # Use the urlopen function from the standard Python 3 library
        response = urlopen(url)
        # Make sure that we are looking at HTML and not other things that
        # are floating around on the internet (such as
        # JavaScript files, CSS, or .PDFs for example)
        if response.getheader('Content-Type')=='text/html; charset=utf-8':
            htmlBytes = response.read()
            # Note that feed() handles Strings well, but not bytes
            # (A change from Python 2.x to Python 3.x)
            htmlString = htmlBytes.decode("utf-8")
            end = 0
            while end >= 0:
                start = htmlString.find('<p class="zn-body__paragraph">"', end)
                end = htmlString.find('</p>', start)
                print(start, end, htmlString[start+30:end], "\n")
            self.feed(htmlString)
            return htmlString, self.links
        else:
            print("Done fucked up")
            return "",[]

# And finally here is our spider. It takes in an URL, a word to find,
# and the number of pages to search through before giving up
# from: http://www.netinstructions.com/how-to-make-a-web-crawler-in-under-50-lines-of-python-code/

def crimeCrawler(url, wordBank, maxPages):  
    pagesToVisit = [url]
    numberVisited = 0
    # The main loop. Create a LinkParser and get all the links on the page.
    # Also search the page for the word or string
    # In our getLinks function we return the web page
    # (this is useful for searching for the word)
    # and we return a set of links from that web page
    # (this is useful for where to go next)
    while numberVisited < maxPages and pagesToVisit != []:
        numberVisited = numberVisited +1
        # Start from the beginning of our collection of pages to visit:
        url = pagesToVisit[0]
        pagesToVisit = pagesToVisit[1:]

        print(numberVisited, "Visiting:", url)
        parser = LinkParser()
        data, links = parser.getLinks(url) #links should only be links to articles
        for word in wordBank: 
            wordScore = data.find(word)
            pagesToVisit = pagesToVisit + links


def getWordBank(pathToWordBank):
    wordBankFile = open(pathToWordBank, 'r')
    wordBank = []
    
    for line in wordBankFile:
        line = line.strip('\n')
        wordBank.append(line)
    
    return wordBank

crimeCrawler("http://www.cnn.com/2016/02/18/world/uganda-election-social-media-shutdown/index.html", ['section class="zn zn-body-text'], 1)