import scrapy
import sys
from urllib.parse import urljoin
from pymongo import MongoClient
from helpers import createEntry,downloadImage


class craigCrawler(scrapy.Spider):
    name = "craigCrawler"
    start_urls = []
    posts = []
    outputTo = ""

    def __init__(self, in_starturls,in_output):
        super(craigCrawler, self).__init__()
        self.start_urls = in_starturls

        #set up mongodb
        client = MongoClient()
        self.collection = client['arbitragedb'].craigslist

        #reroute output
        if(in_output == ""):
            print("Invalid output file")
            exit(1)
        else:
            self.outputTo = in_output

    #parse the url
    def parse(self, response):
        url_list = []

        #get each post
        for result in response.css('li.result-row a::attr(href)').extract():
            if(result != "#" and result not in url_list):

                #if we get an interrupt, exit
                if( self.collection.find({"pid":str(self.scrapPID(result))}).count() > 0 ):
                    return None
                else:
                    yield scrapy.Request(result,callback=self.parsePage)

        #get the next page if it exists
        next = response.css('a.next::attr(href)').get()
        if(next is not None):
            yield scrapy.Request(response.urljoin(next),callback=self.parse)





    #scrape the posts page for what we need
    def parsePage(self, response):
        price = response.css('span.price::text').extract_first()
        title = response.css('#titletextonly::text').extract_first()
        image = response.css('div.swipe-wrap div.first img::attr(src)').extract_first()
        link = response.request.url
        pid = self.scrapPID(link)

        #make sure price is listed
        if(price is None):
            return

        #store in the database
        entry = createEntry(pid,title,price,link)
        if(entry == None):
            return
        else:
            downloadImage(image,pid)

            key = {'pid': entry['pid']}
            self.collection.update_one(key, {'$set':entry}, upsert=True)
            print("Item added: " + entry['pid'])


    #gets the pid from the url
    def scrapPID(self,url):
        rurl = url[::-1]
        start = rurl.find('.')
        end = rurl.find('/') -1
        return rurl[end:start:-1]
