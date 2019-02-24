import scrapy
import sys
from urllib.parse import urljoin
from pymongo import MongoClient
from helpers import *
from arbdb import *
from statistics import median


class ebayCrawler(scrapy.Spider):
    name = "craigCrawler"
    start_urls = ["https://www.ebay.com/"]
    posts = []


    def __init__(self,in_pid):
        super(ebayCrawler, self).__init__()
        self.searchPid = in_pid


    #parse the url
    def parse(self, response):
        #get the item title from craigslist db
        searchItem = readFromCraigDB(self.searchPid)
        if(searchItem == None):
            return


        #search ebay
        return scrapy.FormRequest.from_response(
            response,
            formdata={'_nkw': searchItem['title']},
            callback=self.scrapeResults
        )

    def scrapeResults(self, response):
        #have to get num results to filter out related searches
        results = response.css('h1.srp-controls__count-heading::text').extract_first()
        numResults = -1
        prices = []

        if(results==None):
            return
        else:
            numResults = int(results[:results.find(' ')].rstrip())

        cntr = 0
        for entry in response.css('span.s-item__price::text').extract():

            #if we have gone through all relevant searches exit
            if(cntr >= numResults):
                break
            cntr+=1

            if(entry == None):
                print("Error in scrapeResults algorithm")
                exit(1)

            prices.append(float(entry.replace('$','')))
            prices.sort()

        print(median(prices))
