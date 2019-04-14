import logging
LOG = logging.getLogger("__main__")

from pymongo import MongoClient
import arbHelpers
import datetime
import sys


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
                status = collection.update_one(key,{"$set":entry},upsert=True)

                #sanity check
                if(status.acknowledged == False):
                    LOG.error("Error writing Craigslist")

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
        LOG.error("Error in writeToEbay")
        return

    #connect to DB
    client = MongoClient()
    collection = client['arbitragedb'].ebay

    #write to db
    entry = {"pid": pid, "estimatedPrice": estimatedPrice, "keywords": keywords, "url": url, "timestamp": str(datetime.datetime.utcnow())}
    key = {"pid": pid}
    status = collection.update_one(key,{"$set": entry},upsert=True)

    #sanity check
    if(status.acknowledged == False):
        LOG.error("Error writing Ebay")


def writeArb(item):
    currentcol = arbHelpers.getDate()

    #connect to DB
    client = MongoClient()
    collection = client['arbitragedb'][str(currentcol) + "_arbs"]
    key = {"pid": item['pid']}
    status = collection.update_one(key, {"$set":item}, upsert=True)

    #sanity check
    if(status.acknowledged == False):
        LOG.error("Error writing Arbitrage")

#gives data, sorted by the best arbitrage at top, based on date
def readArb(date, maxPrice = sys.maxsize, minProfit = 0):
    currentcol = date

    #connect to DB
    client = MongoClient()
    collection = client['arbitragedb'][str(currentcol) + "_arbs"]

    #return and sort by descending
    retVal = collection.find({ "$and" :
        [
            {"craigslistPrice": {"$lte": maxPrice}},
            {"arbPrice" : {"$gte": minProfit }}
        ]
    }).sort("arbPrice",-1)

    return retVal
