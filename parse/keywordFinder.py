from collections import *
from math import *
import string
import os

def getArticles():
    '''
    Open all files in the primer texts for training in looking for key indicators
    of desired topic
    '''
    path = '/home/ubuntu/workspace/parse/primerTexts'
    articles = []
    for filename in os.listdir(path):
        articles.append(open("./primerTexts/" + filename, "r"))
    return articles

def cleanIgnoreList():
    ''' 
    Got top 250 most common english words from http://www.wordfrequency.info/free.asp?s=y
    Clean out white space and other extraneous data for ease in comparison
    '''
    ignoreFile = open("./ignore.txt", "r")
    ignore =[]
    for line in ignoreFile:
        sample = line.split("\t")
        noWhiteSpace = ""
        for char in sample[1]:
            if char != " ":
                noWhiteSpace += (char)
        ignore.append(noWhiteSpace)
        
    ignoreFile.close()
    ignoreFile = open("./ignore.txt", "w")
    for word in ignore:
        ignoreFile.write(word + "\n")
    ignoreFile.close()

def getIgnoreList():
    ''' 
    Open and return a list of words to ignore from an already cleaned file of 
    ignore words
    '''
    ignoreFile = open("./ignore.txt", "r")
    ignoreWords = []
    for line in ignoreFile:
        ignoreWords.append(line[0:-1])
    return ignoreWords
    
def cleanWord(word):
    '''
    Strip out any punctuation and cast to lowercase
    '''
    word.lower()
    out = word.translate(string.punctuation)
    return out

def getUniqueArticleText(articles):
    ''' 
    Pull out unique and interesting article text that occurs accross a large 
    proportion of primer articles
    '''
    wordDict = defaultdict(int)
    ignoreWords = getIgnoreList()
    for article in articles:
        seen = []
        for line in article:
            wordArray = line.split(" ")
            for word in wordArray:
                word = cleanWord(word)
                if word not in seen:
                    if len(word) > 2 and word[0:-1] not in seen:
                        if word not in ignoreWords:
                            seen.append(word)
                            wordDict[word] += 1
                    
    articleText = list(wordDict.items())
    return articleText 

def generateWordBank():
    '''
    Generate a list of words and save them to file for reference by the scraper
    '''
    articles = getArticles()
    articleText = getUniqueArticleText(articles)
    bestWords = []
    for wordval in articleText:
        if wordval[1] > ceil(len(articles) /2):
            if len(wordval[0]) > 4:
                bestWords.append(wordval[0])
    goodWords = open('./wordbank.txt', 'w')
    for word in bestWords:
        goodWords.write(word + "\n")
    goodWords.close()
            
    






    





