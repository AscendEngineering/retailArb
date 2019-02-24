#!/usr/bin/env python

from arb import craigCrawler
from scrapy.crawler import CrawlerProcess
import scrapy
import tempfile
from pymongo import MongoClient
import re
import urllib.request
import constants
from image_comp import most_similar
from arbdb import writeToCraigDB,readFromCraigDB
from ebayCrawler import ebayCrawler


def main():

    #create tempfile to store output
    file = tempfile.mkstemp()
    filename = file[1]

    # #run crawler
    # urls_to_crawl = collectUrls()
    # runCraigCrawler(urls_to_crawl,"output.txt")

    #run ebay crawler to look at each item that we pulled
    #ebayLookup("output.txt")

    runEbayCrawler("6817367571")



def ebayLookup(inputfile):

    #for every entry in the file
    itemList = open(inputfile,'r')
    for entry in itemList:
        #get the title from mongodb
        title = readFromCraigDB(entry.rstrip())['title']

        #look up with that search title on ebay



        #if there are results process them



def runCraigCrawler(urls_to_crawl,outputfile):
    print("Running Craigslist Crawler")
    process = CrawlerProcess({
        'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)'
    })


    process.crawl(craigCrawler,urls_to_crawl,outputfile) #change this file to "outputfile"
    process.start()

    print("Crawler finished")


def runEbayCrawler(keyword):
    print("Running Ebay Crawler")
    process = CrawlerProcess({
        'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)'
    })

    process.crawl(ebayCrawler,keyword)
    process.start()


def collectUrls():
    retVal = []

    for item in constants.items:
        print(constants.template + urllib.request.quote(item))
        retVal.append(constants.template + urllib.request.quote(item))

    return retVal



if __name__ == '__main__':
    main()
