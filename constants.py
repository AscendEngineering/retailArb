
distance = 5

template = "https://chicago.craigslist.org/search/sss?sort=date&search_distance="+str(distance)+"&postal=60657&query="
category_template = "https://chicago.craigslist.org/search/{}?search_distance="+str(distance)+"&postal=60657"

imagesFolder = 'images/'

scrapy_output="/logs/scrapy"
program_journal="/logs/program_journal"

items = [
"mug",
"matchbox",
"Fossil",
"Hilfiger",
"Lacoste",
"Converse",
"Nike",
"Adidas",
"Puma",
"Louis Vuitton",
"Reebok",
"jersey",
"toy",
"hockey stick",
"lacrosse stick",
"diabetic test strips",
"fitness tracker",
"xbox",
"ps4",
"ps3",
"ps2",
"360",
"playstation",
"headphones",
"hot wheels",
"stuffed animal",
"ornament",
"hangbag",
"Garmin Forerunner",
"Timex Ironman",
"Suunto Spartan Ultra",
"Apple Watch",
"FitBit",
"Polar M430",
"curtains",
"dewalt",
"bosch",
"makita",
"craftsman",
"ryobi",
"milwaukee",
"rigid",
"black n decker",
"lenox",
"stihl"
]

search_categories = {
    "antiques": "ata" ,
    "appliances": "ppa" ,
    "auto parts": "pta" ,
    "beauty+hlth": "haa",
    "cell phones": "moa",
    "collectibles": "cba",
    "computer parts": "syp",
    "computers": "sya" ,
    "electronics": "ela",
    "jewelry": "jwa",
    "photo/video": "pha",
    "tools": "tla",
    "toys & games": "taa",
}

resultsFolder = 'arb_results/'

arbItemHeaders = ["ebayKeywords","craigslistKeywords","arbPrice","ebayPrice","craigslistPrice","ebayUrl","craigslistUrl","pid"]

outfiles = "outfiles/"

daysSaved=7

max_price=500
