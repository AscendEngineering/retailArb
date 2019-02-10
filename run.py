from arb import craigCrawler
from scrapy.crawler import CrawlerProcess
import scrapy
import tempfile
from pymongo import MongoClient
import re
import urllib.request
import constants

def main():

    #create tempfile to store output
    file = tempfile.mkstemp()
    filename = file[1]

    #run crawler
    urls_to_crawl = collectUrls()
    runCraigCrawler(urls_to_crawl,"output.txt")

    #run google crawler to look at each item that we pulled
    ebayLookup("output.txt",)



def ebayLookup(inputfile):

    #for every entry in the file
    print("")



def runCraigCrawler(urls_to_crawl,outputfile):
    print("Running Crawler")
    process = CrawlerProcess({
        'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)'
    })


    process.crawl(craigCrawler,urls_to_crawl,outputfile) #change this file to "outputfile"
    process.start()

    print("Crawler finished")




def collectUrls():
    retVal = []

    for item in constants.items:
        print(constants.template + urllib.request.quote(item))
        retVal.append(constants.template + urllib.request.quote(item))

    return retVal



def writeToDB(filename):
    print("Writing to DB...")
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


    print("Finished DB")

if __name__ == '__main__':
    main()
