import scrapy
from urllib.parse import urljoin

class craigCrawler(scrapy.Spider):
    name = "runArb"
    start_urls = [
        'https://chicago.craigslist.org/search/sss?query=mugs&sort=rel'
    ]
    posts = []

    def parse(self, response):
        url_list = []
        #self.collectNextPage(response)
        for result in response.css('li.result-row a::attr(href)').extract():
            if(result != "#" and result not in url_list):
                #url_list.append(result)
                yield scrapy.Request(result,callback=self.parsePage)

        next = response.css('a.next::attr(href)').get()
        print(next)
        if(next is not None):
            yield scrapy.Request(response.urljoin(next),callback=self.parse)

    def parsePage(self, response):
        price = response.css('span.price::text').extract_first()
        title = response.css('#titletextonly::text').extract_first()
        if(price is None):
            price = ""
        if(title is None):
            title = ""
        print(title + ": " + price + " - \n\t " + response.request.url)

        #if there is another page add it to the start_urls list

    def getposts():
        #get original posts
        posts = response.css('li.result-row a::attr(href)').extract()


    def collectNextPage(self,response):

        #if there is an href for the next page, grab it
        next = response.css('a.next::attr(href)').get()
        if(next is not None):
            yield scrapy.Request(urljoin(response.urljoin(next)),callback=self.parse)
