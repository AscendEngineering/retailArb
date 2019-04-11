
distance = 15

template = "https://chicago.craigslist.org/search/sss?sort=date&search_distance="+str(distance)+"&postal=60657&query="

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
#"iphone",
#"samsung",
"diabetic test strips",
"fitness tracker",
#"Apple",
"xbox",
"ps4",
"ps3",
"ps2",
"360",
"playstation",
#"airpods",
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
"curtains"

]

resultsFolder = 'arb_results/'

arbItemHeaders = ["ebayKeywords","craigslistKeywords","arbPrice","ebayPrice","craigslistPrice","ebayUrl","craigslistUrl","pid"]

outfiles = "outfiles/"

daysSaved=7

max_price=500
