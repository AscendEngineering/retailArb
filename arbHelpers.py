import logging
LOG = logging.getLogger("__main__")

import urllib.request
import re
import constants
import os.path
from urllib.parse import urlparse,parse_qs
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords
from nltk.tokenize import RegexpTokenizer
import nltk
from arbdb import readFromCraigDB,readFromEbayDB
import datetime
import generateSearchTerms

#entry that will be stored in db
def createEntry(pid,title,price,query,format,link):
    price = re.sub("[^0-9]","", price)
    if(price == ""):
        price = "-1"

    retVal = {
        'pid': pid,
        'title': title,
        'price': int(price),
        'query': query,
        'format':format,
        'url': link,
        'timestamp': str(datetime.datetime.utcnow())
    }

    return retVal

def getFileFormat(file):
    temp = file[::-1]
    temp = temp[:temp.find('.')]
    return temp[::-1]

def downloadImage(src, name):
    format = getFileFormat(src)
    filelocation = constants.imagesFolder + name + '.' + format

    #file exists check
    if(os.path.isfile(filelocation)):
        return
    else:
        urllib.request.urlretrieve(src,filelocation)

def getQuery(url):
    parsed = urlparse(url)
    return urllib.parse.parse_qs(parsed[4])['query'][0]

def collectUrls():
    retVal = []
    #search term urls
    items = generateSearchTerms.getAllItems()

    for item in items:
        LOG.info(constants.template + urllib.request.quote(item))
        retVal.append(constants.template + urllib.request.quote(item))

    #craigslist categories
    for key,value in constants.search_categories.items():
        category_url = (constants.category_template).format(value)
        LOG.info(category_url)
        retVal.append(category_url)

    return retVal

def removeStopWords(keywords):
    #implement here
    stopWords = set(stopwords.words('english'))
    words = word_tokenize(keywords)
    wordsFiltered = []

    for w in words:
        if w not in stopWords:
            wordsFiltered.append(w)

    return ' '.join(wordsFiltered)

def removeNumbers(keywords):

    words = keywords.split(' ')
    filteredWords = []

    for word in words:
        if(word.isnumeric()):
            continue
        else:
            filteredWords.append(word)

    return ' '.join(filteredWords)

def removeSymbols(keywords):
    tokenizer = RegexpTokenizer(r'\w+')
    wordList = tokenizer.tokenize(keywords)

    return ' '.join(wordList)

def removeAdj(keywords):
    words = word_tokenize(keywords)
    tagged = nltk.pos_tag(words)
    retVal = []

    for tag in tagged:
        if(tag[1]=='JJ' or tag[1]=='ADJ'):
            continue
        else:
            retVal.append(tag[0])

    return ' '.join(retVal)

def getEbaySearchKeywords(url,keyword):
    parsed = urlparse(url)
    retVal=[""]
    try:
        retVal = (urllib.parse.parse_qs(parsed.query))[keyword]
    except KeyError as e:
        LOG.info("Keyword " + keyword + " does not exist")

    return retVal[0]


def detectArbitrage(pid):
    ebayData = readFromEbayDB(pid)
    craigslistData = readFromCraigDB(pid)
    retVal = None

    if(ebayData==None or craigslistData==None):
        LOG.error("Error in reading DB for detectArbitrage(): " + str(pid))
        return None

    if(ebayData["estimatedPrice"] >= craigslistData["price"]):
        retVal = {
            "pid": ebayData["pid"],
            "arbPrice": (ebayData["estimatedPrice"] - craigslistData["price"]),
            "ebayPrice": ebayData["estimatedPrice"],
            "craigslistPrice": craigslistData["price"],
            "ebayUrl": ebayData["url"],
            "craigslistUrl": craigslistData["url"],
            "ebayKeywords":ebayData["keywords"],
            "craigslistKeywords":craigslistData["title"],
            "timestamp": str(datetime.datetime.utcnow())
        }

    return retVal


def getDate():
    return str(datetime.datetime.today()).split(' ')[0].replace('-','')

def generateFilename():
    return str(datetime.datetime.today()).replace('-','').replace(':','').replace(' ','-').split('.')[0]

def getFloatNum(input):
    input=input.rstrip()
    num = ""
    for char in input:
        if(char.isdigit()):
            num += char
        elif(char == '.'):
            num += char
    if(len(num) <= 2):
        num+=".00"
    return float(num)

def getIntNum(input):
    input=input.rstrip()
    num = ""
    for char in input:
        if(char.isdigit()):
            num += char
    return int(num)
