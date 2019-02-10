import urllib.request
import re
import constants


#entry that will be stored in db
def createEntry(pid,title,price,link):
    price = re.sub("[^0-9]","", price)
    if(price == ""):
        return None

    retVal = {
        'title': title,
        'price': int(price),
        'link': link,
        'pid': pid
    }

    return retVal


def getFileFormat(file):
    temp = file[::-1]
    temp = temp[:temp.find('.')]
    return temp[::-1]

def downloadImage(src, name):
    #get the file format
    format = getFileFormat(src)
    #form the file location

    filelocation = constants.imagesFolder + name + '.' + format
    urllib.request.urlretrieve(src,filelocation)
