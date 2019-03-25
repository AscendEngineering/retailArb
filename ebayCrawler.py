import scrapy
import sys
from urllib.parse import urljoin
from pymongo import MongoClient
import arbHelpers
from arbdb import *
from statistics import median
from user_agent import generate_user_agent


class ebayCrawler(scrapy.Spider):
    name = "ebayCrawler"
    start_urls = ["https://www.ebay.com/sch/ebayadvsearch"]
    custom_settings={
        'COOKIES_ENABLED': False,
        'USER_AGENT': generate_user_agent(),
        'LOG_ENABLED': False
    }


    def __init__(self,in_pid):
        super(ebayCrawler, self).__init__()
        self.searchPid = in_pid

    #parse the url
    def parse(self, response):
        #get the item title from craigslist db
        searchItem = readFromCraigDB(self.searchPid)
        if(searchItem == None):
            print("Error in reading from CraigslistDb: " + self.searchPid)
            return

        #search ebay
        return scrapy.FormRequest.from_response(
            response,
            formdata={'_nkw': searchItem['title'],'LH_ItemCondition':'4'}, #second argument is for used products
            meta={"iter": 0},
            callback=self.scrapeResults
        )

    def scrapeResults(self, response):
        print("Ebay Searching URL: " + response.request.url)
        #have to get num results to filter out related searches
        results = response.css('#cbelm > div.clt > h1 > span.rcnt::text').extract_first()
        keywords = arbHelpers.getEbaySearchKeywords(response.request.url,'_nkw')
        numResults = -1
        prices = []

        #if there are no results still enter empty result in db
        if(results==None):
            print("No Results Found(" + str(iter) + "): " + keywords)
            writeToEbayDB(self.searchPid,-1,keywords,response.request.url)
            return
        else:
            numResults = int(results)

        #if we do not have any results, modify keywords and try again
        if(numResults==0):
            newQuery=""
            iter = response.request.meta['iter']

            #if we are on the first iteration, remove symbols and stop words
            if(iter == 0):
                newQuery = arbHelpers.removeStopWords(arbHelpers.removeSymbols(keywords))

            #if we are on the second iteration, remove numbers
            if(iter == 1):
                newQuery = arbHelpers.removeNumbers(keywords)

            #if we are on the last iteration exit out
            if(iter == 2):
                print("No Results Found(" + str(iter) + "): " + keywords)
                writeToEbayDB(self.searchPid,-1,keywords,response.request.url)
                return

            print("Refining Search (" + str(iter) + "): " + keywords)
            return scrapy.FormRequest.from_response(
                response,
                formdata={'_nkw': newQuery},
                meta={"iter": iter+1},
                dont_filter=True,
                callback=self.scrapeResults
            )


        #get the median price
        cntr = 0
        for entry in response.css('li.lvprice.prc > span.bold::text').extract():

            #if we have gone through all relevant searches exit
            if(cntr >= numResults):
                break
            cntr+=1

            if(entry == None):
                print("Error in scrapeResults algorithm")
                exit(1)

            prices.append(arbHelpers.getFloatNum(entry))

            prices.sort()

        #median price because I do not want a large outlier to throw of the target value
        medianPrice = median(prices)

        #store the estimated price in the databbase
        print("Ebay Item Found: " + self.searchPid)
        writeToEbayDB(self.searchPid,medianPrice,keywords,response.request.url)
