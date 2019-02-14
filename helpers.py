import urllib.request
import re
import constants
import os.path
from urllib.parse import urlparse


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
        'link': link,

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
