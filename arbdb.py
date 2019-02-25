from pymongo import MongoClient


def writeToCraigDB(filename):
    print("Writing to Craisglist DB...")
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
    retVal = db.craigslist.find_one({"pid" : pid })

    return retVal

def writeToEbayDB(pid,estimatedPrice):

    #sanity check
    if(pid == None or estimatedPrice==0):
        print("Error in writeToEbay")
        return

    print("Writing to Ebay DB...")

    #connect to DB
    client = MongoClient()
    collection = client['arbitragedb'].ebay

    #write to db
    entry = {"pid": pid, "estimatedPrice": estimatedPrice}
    key = {"pid": pid}
    collection.update(key,entry,upsert=True)
