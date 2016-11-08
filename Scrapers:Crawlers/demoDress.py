from bs4 import BeautifulSoup
import urllib
import urllib2
import requests
import json

from pymongo import MongoClient
client = MongoClient('mongodb://trossi:1460@ds143707.mlab.com:43707/heroku_b37frt6h')
db = client.heroku_b37frt6h
f21 = db.f21
f21.create_index([("name", "text"), ("brand", "text")])

def findBrand(soup):
	return "Forever21"

def findPrice(soup):
	priceArray = soup.findAll('span', {"itemprop" : "price"})
	if priceArray is not None:
		for price in priceArray:
			return price.text
	return ""

def findProductName(soup):
	product = soup.find('h1', class_='item_name_p')
	if product is not None:
		return product.text
	return ""

def findImageLink(soup):
	image = soup.find('meta', {"property" : "og:image"})
	if image is not None:
		return image['content']
	return ""

def findDescription(soup):
	description = soup.find('meta', {"property" : "og:description"})
	if description is not None:
		return description['content']
	return ""

# def findUrl(soup):
# 	url = soup.find('meta', {"property" : "og:url"})
# 	if url is not None:
# 		return url['content']
# 	return ""

def postProduct(url):
	html = urllib.urlopen(url).read()
	soup = BeautifulSoup(html, "html.parser")
	product = {'brand': findBrand(soup), 'name': findProductName(soup), 'price': findPrice(soup), 'image': findImageLink(soup), 'description': findDescription(soup), 'url': url}
	f21.insert(product)


bigMenu = [u'f21', u'21men', u'plus', u'girls', u'boys']
menuesf21 = [u'dress', u'top_blouses', u'outerwear_coats-and-jackets', u'bottoms', u'intimates_loungewear', u'activewear', u'swimwear_all', u'acc', u'shoes', u'branded-shop-women-clothing']
menuesMen = [u'mens-tops', u'mens-tees-tanks-graphic', u'mens-jackets-and-coats', u'mens-bottom', u'mens-accessories', u'mens-shoes', u'branded-shop-men']
menuesPlus = [u'plus_size-dresses', u'plus_size-tops', u'plus_size-outerwear', u'plus_size-bottom', u'plus_size-intimates', u'plus_size-swimwear', u'plus_size-activewear']
menuesGirls = [u'girls_dresses-rompers', u'girls_tops', u'girls_outerwear', u'girls_bottom', u'girls_accessories']
menuesBoys = [u'boys_main']
overallMenu = [menuesf21, menuesMen, menuesPlus, menuesGirls, menuesBoys]

noPage = ["mens-jackets-and-coats", "mens-bottom", "mens-shoes", "plus_size-intimates", 'girls_dresses-rompers', 'girls_tops', 'girls_outerwear', 'girls_bottom', 'girls_accessories', "boys_main"]


params = {"action": "getcategory",
          "br": "f21",
          "category": menuesf21[0],
          "pageno": 1,
          "pagesize": "",
          "sort": "",
          "fsize": "",
          "fcolor": "",
          "fprice": "",
          "fattr": ""}

url = "http://www.forever21.com/Ajax/Ajax_Category.aspx"
test = requests.get(url, params=params)
js = requests.get(url, params=params).json()

i = 0
j = 0
menuIndex = 0
bigMenuIndex = 0

while bigMenuIndex < len(bigMenu):
  params["br"] = bigMenu[bigMenuIndex]
  print params["br"]
  menues = overallMenu[bigMenuIndex]
  while menuIndex < len(menues):
    params["category"] = menues[menuIndex]
    print params["category"]
    params["pageno"] = 1
    js = requests.get(url, params=params).json()
    soup = BeautifulSoup(js[u'CategoryHTML'], "html.parser")
    while len(soup.select("div.item_pic a")) != 0:
      for a in soup.select("div.item_pic a"):
        postProduct(a["href"])
        i = i + 1
        j = j + 1
      if (params["category"] in noPage):
        break
      params["pageno"] = params["pageno"] + 1
      js = requests.get(url, params=params).json()
      soup = BeautifulSoup(js[u'CategoryHTML'], "html.parser")
    menuIndex = menuIndex + 1
    print i
    i = 0
  bigMenuIndex = bigMenuIndex + 1
  menuIndex = 0

print i
print j
print "done"



