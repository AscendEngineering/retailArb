from datetime import datetime,timedelta
from pymongo import MongoClient
from arbHelpers import getIntNum
import constants

def main():



    #get todays date from 7 days ago
    cutoffDate = str(datetime.now() - timedelta(days=constants.daysSaved))
    print("Deleting dates earlier than: " + cutoffDate + "\n")

    #go through the two databases and clean
    client = MongoClient()
    db = client['arbitragedb']
    collections = db.collection_names()

    #clean each collection
    for collection in collections:
        print("Cleaning " + collection + "...")
        cleanDatabase(collection, cutoffDate)


    print("Done")

def cleanDatabase(collection, cutoffDate):

    #get all entries with the timestamp that is
    client = MongoClient()
    results = client['arbitragedb'][collection].delete_many({"timestamp": {"$lt": cutoffDate}})
    print("Deleted " + str(results.deleted_count) + " records\n")




if __name__ == '__main__':
    main()
