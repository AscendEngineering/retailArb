import argparse
from arbHelpers import getDate,generateFilename
import csv
import datetime
import constants
from arbdb import readArb
import sys

def main():
    parser = argparse.ArgumentParser(description='Grabbing Arbitrages Tool')
    parser.add_argument("--date","-d",help="specify the date you want to pull from (We only save 7 days back)", default=getDate())
    parser.add_argument("--maxprice",type=int, help="max price to pay",default=sys.maxsize)
    parser.add_argument("--minprofit",type=int, help="min profit to make",default=0)
    parser.add_argument("--percentProfit","-pp",type=float, help="percent profit you would like to make",default=0.0)
    args = parser.parse_args()

    #variables
    date = args.date
    maxPrice = args.maxprice
    minProfit = args.minprofit
    percentProfit = args.percentProfit


    #collectAll Arbs
    file = constants.resultsFolder+generateFilename()+".csv"
    collectArbs(file,date,maxPrice,minProfit,percentProfit)
    print(file)

def collectArbs(file,date,maxPrice,minProfit,percentProfit):

    #open up the csv, write headers
    with open(file,'w',newline='') as csvfile:
        writer = csv.writer(csvfile,delimiter=',')
        writer.writerow(constants.arbItemHeaders)

        #get the results and write them
        results = readArb(date, maxPrice, minProfit)
        for result in results:
            itemList = getItemList(result,percentProfit)

            #write to csv
            if(len(itemList)>0):
                writer.writerow(itemList)


def getItemList(arbItem,percentProfit = 0.0):
    retVal = []
    for item in constants.arbItemHeaders:

        #percentage profit
        if( arbItem["arbPrice"] >= float(arbItem["craigslistPrice"]) * (percentProfit/100.0)):
            retVal.append(arbItem[item])

    return retVal





if __name__ == '__main__':
    main()
