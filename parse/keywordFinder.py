from collections import *
from math import *

articles = [open("./mikebrown.txt","r"),open("./tamir.txt","r"),
    open("./jamar.txt","r"), open("./shooting.txt", "r"), open("./bland.txt")]
wordDict = defaultdict(int)
for article in articles:
    seen = []
    for line in article:
        wordArray = line.split(" ")
        for word in wordArray:
            if word not in seen:
                seen.append(word)
                wordDict[word] += 1

ignoreFile = open("./ignore.txt", "r")
for line in ignoreFile:
    sample = line.split("\t")
    noWhiteSpace = ""
    for char in sample[1]:
        if char != " ":
            noWhiteSpace += (char)
    print(noWhiteSpace)

allWords = list(wordDict.items())
bestWords = []
for wordval in allWords:
    if wordval[1] > ceil(len(articles) /2):
        if len(wordval[0]) > 4:
            bestWords.append(wordval[0])
goodWords = open('./wordbank.txt', 'w')
for word in bestWords:
    goodWords.write(word + "\n")
goodWords.close()

print bestWords
            
    





