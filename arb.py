import scrapy
import sys
from urllib.parse import urljoin
from pymongo import MongoClient
from arbHelpers import *


class craigCrawler(scrapy.Spider):
    name = "craigCrawler"
    start_urls = []
    posts = []
    outputPID = []

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
        query = getQuery(response.request.url)

        #get each post
        for result in response.css('li.result-row a::attr(href)').extract():
            if(result != "#" and result not in url_list):

                #if item is already there do not add it, if it matches the query exit out
                if( self.collection.find({"pid":str(self.scrapPID(result))}).count() > 0 ):
                    for page in self.collection.find({"pid":str(self.scrapPID(result))}):
                        if(page['query'] == query):
                            return None
                    break

                #get the posts from the page
                yield scrapy.Request(result,callback=self.parsePage,meta = {'query':query})

        #get the next page if it exists
        next = response.css('a.next::attr(href)').get()
        if(next is not None):
            yield scrapy.Request(response.urljoin(next),callback=self.parse)



    #scrape the posts page for what we need
    def parsePage(self, response):

        #filter non-priced entries
        price = response.css('span.price::text').extract_first()
        if(price is None):
            return

        #grab elements
        title = response.css('#titletextonly::text').extract_first()
        image = response.css('div.swipe-wrap div.first img::attr(src)').extract_first()
        link = response.request.url
        pid = self.scrapPID(link)
        query = response.request.meta['query']
        format = "" if image=="" else getFileFormat(image)

        #store in the database
        entry = createEntry(pid,title,price,query,format,link)
        #downloadImage(image,pid) #we might need this later

        print("Item found: " + str(pid))

        key = {'pid': entry['pid']}
        self.collection.update_one(key, {'$set':entry}, upsert=True)

        #print pid to file to have it later
        fout = open(self.outputTo,'a')
        fout.write(pid + '\n')
        fout.close()

    #gets the pid from the url
    def scrapPID(self,url):
        rurl = url[::-1]
        start = rurl.find('.')
        end = rurl.find('/') -1
        return rurl[end:start:-1]
