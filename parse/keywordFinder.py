from collections import *
from math import *
import string
import os

def getArticles():
    path = '/home/ubuntu/workspace/parse/primerTexts'
    articles = []
    for filename in os.listdir(path):
        articles.append(open("./primerTexts/" + filename, "r"))
    return articles
#articles = [open("./primerTexts/mikebrown.txt","r"),open("./primerTexts/tamir.txt","r"),
#    open("./primerTexts/jamar.txt","r"), open("./primerTexts/shooting.txt", "r"), open("./bland.txt")]

def cleanIgnoreList():
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
    ignoreFile = open("./ignore.txt", "r")
    ignoreWords = []
    for line in ignoreFile:
        ignoreWords.append(line[0:-1])
    return ignoreWords
    
def cleanWord(word):
    word.lower()
    out = word.translate(string.punctuation)
    return out

def getUniqueArticleText(articles):
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
            
    






    





