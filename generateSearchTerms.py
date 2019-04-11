# import urllib.parse
# import urllib.request
# import gzip

import requests
import json
import pprint
import constants

def main():
    print(getAllItems)


def getAllItems():
    items = []
    items += getTrendingEbay()
    items += getStaticEntry()

    return(items)

def getTrendingEbay():

    #form request
    headers = {
        'Origin': 'https://explore.ebay.com',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'en-US,en;q=0.9',
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36',
        'Content-Type': 'application/json;charset=UTF-8',
        'Accept': 'application/json, text/plain, */*',
        'Referer': 'https://explore.ebay.com/',
        'Connection': 'keep-alive',
    }
    data = '{"keyword":"all","siteID":"0"}'

    #send,convert to json
    response = requests.post('https://explore.ebay.com/api/trending/userInput', headers=headers, data=data)
    jsonData = json.loads(response.text)

    #add to list and return
    items = []
    for item in jsonData:
        items.append(item['_source']['story_title_txt'])

    return(items)

def getStaticEntry():
    return(constants.items)


if __name__ == '__main__':
    main()
