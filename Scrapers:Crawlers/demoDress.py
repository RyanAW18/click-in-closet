from bs4 import BeautifulSoup
import urllib
import urllib2
import requests
import json

from pymongo import MongoClient
client = MongoClient('mongodb://trossi:1460@ds143707.mlab.com:43707/heroku_b37frt6h')
db = client.heroku_b37frt6h
f21_dresses = db.f21_dresses

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
	f21_dresses.insert(product)


params = {"action": "getcategory",
          "br": "f21",
          "category": "dress",
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
product_soup = BeautifulSoup(js[u'CategoryHTML'], "html.parser")
i = 0
j = 0

while len(product_soup.select("div.item_pic a")) != 0:
	for a in product_soup.select("div.item_pic a"):
		postProduct(a["href"])
		i = i + 1
	params["pageno"] = params["pageno"] + 1
	j = j + 1
	js = requests.get(url, params=params).json()
	product_soup = BeautifulSoup(js[u'CategoryHTML'], "html.parser")

print i
print j
print "done"



