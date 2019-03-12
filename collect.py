import argparse
from arbHelpers import getDate,generateFilename
import csv
import datetime
import constants
from arbdb import readArb

def main():
    parser = argparse.ArgumentParser(description='Grabbing Arbitrages Tool')
    parser.add_argument("--date","-d",help="specify the date you want to pull from (We only save 7 days back)", default=getDate())
    parser.add_argument("-keywords","-s", help="keywords to search", default="")
    args = parser.parse_args()

    #variables
    date = args.date
    keywords = args.keywords

    #collectAll Arbs
    print("Collecting...")
    file = constants.resultsFolder+generateFilename()+".csv"
    collectArbs(file,date,"")
    print("...finished")

def collectArbs(file,date,keywords):

    #open up the csv, write headers
    with open(file,'w',newline='') as csvfile:
        writer = csv.writer(csvfile,delimiter=',')
        writer.writerow(constants.arbItemHeaders)

        #get the results and write them
        results = readArb(date)
        for result in results:
            itemList = getItemList(result)
            writer.writerow(itemList)






def getItemList(arbItem):
    retVal = []
    for item in constants.arbItemHeaders:
        retVal.append(arbItem[item])
    return retVal





if __name__ == '__main__':
    main()
