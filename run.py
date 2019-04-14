#!/usr/bin/env python

#set up logger before calling imports (since they will use it)
import datetime
import logging
LOG = logging.getLogger(__name__)
LOG.setLevel(logging.INFO)
handler = logging.FileHandler('logs/run_logs/'+ str(datetime.datetime.today()).replace('-','').replace(':','').replace(' ','-').split('.')[0])
handler.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s[%(levelname)s]: %(message)s')
handler.setFormatter(formatter)
LOG.addHandler(handler)

logging.getLogger(__name__).addHandler(logging.StreamHandler())


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

    exit(0)
    #configure the Crawler
    configure_logging()
    runner = CrawlerRunner()

    @defer.inlineCallbacks
    def crawl():

        for url in urls_to_crawl:

            outputfile = tempfile.mkstemp()[1]
            LOG.info("Output file: " + outputfile)

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
                    LOG.info("Arbitrage Found: " + pid)
                    writeArb(arbItem)

            os.remove(outputfile)
        reactor.stop()

    #set up the crawlers and run
    crawl()
    reactor.run()


if __name__ == '__main__':
    main()
