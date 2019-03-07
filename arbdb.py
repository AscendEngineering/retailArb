from pymongo import MongoClient
import arbHelpers


def writeToCraigDB(filename):
    #open the database
    client = MongoClient()
    collection = client['arbitragedb'].craigslist

    #open the file
    with open(filename,'r') as file:
        for line in file:
            entry = createEntry(line)
            if(entry == None):
                continue
            else:
                key = {'pid': entry['pid']}
                collection.update(key,entry,upsert=True)

def readFromCraigDB(pid):
    client = MongoClient()
    db = client['arbitragedb']
    retVal = db.craigslist.find_one({"pid": pid.rstrip()})

    return retVal

def readFromEbayDB(pid):
    client = MongoClient()
    db = client['arbitragedb']
    retVal = db.ebay.find_one({"pid": pid.rstrip()})

    return retVal

def writeToEbayDB(pid,estimatedPrice,keywords,url):

    #sanity check
    if(pid == None or estimatedPrice==0):
        print("Error in writeToEbay")
        return

    #connect to DB
    client = MongoClient()
    collection = client['arbitragedb'].ebay

    #write to db
    entry = {"pid": pid, "estimatedPrice": estimatedPrice, "keywords": keywords, "url": url}
    key = {"pid": pid}
    collection.update(key,entry,upsert=True)


def writeArb(item):
    currentcol = arbHelpers.getDate()

    #connect to DB
    client = MongoClient()
    collection = client['arbitragedb'][str(currentcol) + "_arbs"]
    collection.update({"pid":item['pid']},item,upsert=True)
