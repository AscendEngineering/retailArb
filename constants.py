
distance = 15

template = "https://chicago.craigslist.org/search/sss?sort=date&search_distance="+str(distance)+"&postal=60657&query="

imagesFolder = 'images/'

scrapy_output="/logs/scrapy"
program_journal="/logs/program_journal"

items = [
"caffeine"
# "mugs",
# "mug",
# "matchbox",
# "Chanel‎",
# "Dior‎",
# "Gucci‎",
# "Hugo Boss",
# "Burberry",
# "Chanel",
# "Dior Homme",
# "Dolce & Gabbana",
# "Tom Ford",
# "Fossil",
# "Hilfiger",
# "Jimmy Choo Ltd",
# "Kate Spade",
# "Lacoste",
# "Converse",
# "Nike",
# "Adidas",
# "Puma",
# "Louis Vuitton",
# "Reebok",
# "Air Jordan",
# "jersey",
# "toy",
# "toys",
# "hockey stick",
# "lacrosse stick",
# "hockey sticks",
# "lacrosse sticks",
# "iphone",
# "samsung",
# "diabetic test strips",
# "fitness tracker",
# "Apple",
# "xbox",
# "ps4",
# "ps3",
# "ps2",
# "360",
# "playstation",
# "airpods",
# "headphones",
# "hot wheels",
# "stuffed animal",
# "stuffed animals",
# "book"
]

resultsFolder = 'arb_results/'

arbItemHeaders = ["ebayKeywords","craigslistKeywords","arbPrice","ebayPrice","craigslistPrice","ebayUrl","craigslistUrl","pid"]

outfiles = "outfiles/"

daysSaved=7
