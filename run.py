#!/usr/bin/env python

#pyhon libraries
import datetime
import logging
import os
import tempfile
import time
import urllib.request
from scrapy.crawler import CrawlerRunner
from scrapy.utils.log import configure_logging
from twisted.internet import reactor, defer
from pymongo import MongoClient
import argparse
from progress.bar import Bar

#parse args
parser = argparse.ArgumentParser(description='Runs arbitrage')
parser.add_argument("--verbose","-v", action='store_true', help="verbose")
args = parser.parse_args()

#set up logger before calling imports (since they will use it)
LOG = logging.getLogger(__name__)
LOG.setLevel(logging.INFO)
handler = logging.FileHandler('logs/run_logs/'+ str(datetime.datetime.today()).replace('-','').replace(':','').replace(' ','-').split('.')[0])
handler.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s[%(levelname)s]: %(message)s')
handler.setFormatter(formatter)
LOG.addHandler(handler)

#verbose logging to screen (still logs to file)
if(args.verbose):
    logging.getLogger(__name__).addHandler(logging.StreamHandler())


#local files
from arb import craigCrawler
import constants
from arbdb import writeToCraigDB,readFromCraigDB,writeArb
from arbHelpers import *
from ebayCrawler import ebayCrawler


def main():

    #verify that mongodb is running
    try:
        client = MongoClient()
        client.server_info()
    except:
        LOG.error("Mongo Database is not running")
        exit(1)


    #collect urls
    urls_to_crawl = collectUrls()

    if(not args.verbose):
        bar = Bar('Processing', max=len(urls_to_crawl))

    #configure the Crawler
    configure_logging()
    runner = CrawlerRunner()

    @defer.inlineCallbacks
    def crawl():

        for url in urls_to_crawl:
            if(not args.verbose):
                bar.next()

            outputfile = tempfile.mkstemp()[1]
            #LOG.info("Output file: " + outputfile)

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

    #stop progress bar
    if(not args.verbose):
       bar.finish()

if __name__ == '__main__':
    main()
