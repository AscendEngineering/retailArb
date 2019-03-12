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
import os
import tempfile

def main():

    #run crawler
    urls_to_crawl = collectUrls()

    #configure the Crawler
    configure_logging()
    runner = CrawlerRunner()

    @defer.inlineCallbacks
    def crawl():

        for url in urls_to_crawl:

            outputfile = tempfile.mkstemp()[1]

            #run the craigslist crawler
            yield runner.crawl(craigCrawler,[url],outputfile)

            #go through pids and crawl them in ebay
            if os.path.exists(outputfile):
                pidList = open(outputfile,'r')
            else:
                continue

            #go through every found pid in the list
            for pid in pidList:
                pid = pid.rstrip()
                yield runner.crawl(ebayCrawler,pid)

                #detect an arbitrage
                arbItem = detectArbitrage(pid)
                if(arbItem != None):
                    print("Arbitrage Found: " + pid)
                    writeArb(arbItem)

            os.remove(outputfile)
        reactor.stop()

    #set up the crawlers and run
    crawl()
    reactor.run()


if __name__ == '__main__':
    main()
