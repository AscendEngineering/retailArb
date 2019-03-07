import scrapy
import sys
from urllib.parse import urljoin
from pymongo import MongoClient
import arbHelpers
from arbdb import *
from statistics import median


class ebayCrawler(scrapy.Spider):
    name = "ebayCrawler"
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
            print("Error in reading from CraigslistDb: " + self.searchPid)
            return

        #search ebay
        return scrapy.FormRequest.from_response(
            response,
            formdata={'_nkw': searchItem['title']},
            meta={"iter": 0},
            callback=self.scrapeResults
        )

    def scrapeResults(self, response):
        #have to get num results to filter out related searches
        results = response.css('h1.srp-controls__count-heading::text').extract_first()
        keywords = arbHelpers.getEbaySearchKeywords(response.request.url,'_nkw')
        numResults = -1
        prices = []

        if(results==None):
            print("No Results Found(" + str(iter) + "): " + keywords)
            writeToEbayDB(self.searchPid,-1,keywords,response.request.url)
            return
        else:
            numResults = int(results[:results.find(' ')].rstrip().replace(',',''))

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


        cntr = 0
        for entry in response.css('span.s-item__price::text').extract():

            #if we have gone through all relevant searches exit
            if(cntr >= numResults):
                break
            cntr+=1

            if(entry == None):
                print("Error in scrapeResults algorithm")
                exit(1)

            prices.append(float(entry.replace('$','').replace(',','')))

            prices.sort()

        #median price because I do not want a large outlier to throw of the target value
        medianPrice = median(prices)

        #store the estimated price in the databbase
        writeToEbayDB(self.searchPid,medianPrice,keywords,response.request.url)
