#!/usr/bin/env python

from arb import craigCrawler
from scrapy.crawler import CrawlerRunner
from scrapy.utils.log import configure_logging
from twisted.internet import reactor, defer
from pymongo import MongoClient
import urllib.request
import constants
from arbdb import writeToCraigDB,readFromCraigDB,writeArb
from arbHelpers import *
import time
from ebayCrawler import ebayCrawler

def main():

    #run crawler
    urls_to_crawl = collectUrls()

    #configure the Crawler
    configure_logging()
    runner = CrawlerRunner()

    @defer.inlineCallbacks
    def crawl():

        #specify the outfile
        outputfile = "outfile"

        for url in urls_to_crawl:
            #run the craigslist crawler
            yield runner.crawl(craigCrawler,[url],outputfile)

            #go through pids and crawl them in ebay
            pidList = open(outputfile,'r')

            print("Craigslist crawler finished")

            arbItems = []

            for pid in pidList:
                yield runner.crawl(ebayCrawler,pid.rstrip())

                #detect an arbitrage
                arbItem = detectArbitrage(pid)
                if(arbItem != None):
                    print("Arbitrage Found: " + pid)
                    writeArb(arbItem)

        reactor.stop()

    #set up the crawlers and run
    crawl()
    reactor.run()


if __name__ == '__main__':
    main()
