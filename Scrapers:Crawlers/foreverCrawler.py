from bs4 import BeautifulSoup
import urllib
import urllib2
import requests
import json

from pymongo import MongoClient
client = MongoClient('mongodb://trossi:1460@ds143707.mlab.com:43707/heroku_b37frt6h')
db = client.heroku_b37frt6h
products = db.productsMen
products.create_index([("name", "text"), ("brand", "text")])

def findBrand(soup):
	return "Forever 21"

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

def findKeyWords(description, name, brand):
  keyTerms = []
  superString = description + ' ' + name + ' ' + brand
  terms = superString.split(' ')
  for term in terms:
    if term not in commonWords:
      keyTerms.append(term)
  return keyTerms

def postProduct(url, category):
  print "url: " + url
  html = urllib.urlopen(url).read()
  soup = BeautifulSoup(html, "html.parser")
  name = findProductName(soup)
  print "name: " + name
  description = findDescription(soup)
  brand = findBrand(soup)
  nameTerms = name.split(' ')
  for term in nameTerms:
    if term in exceptionList:
      category = exceptionList[term]
  product = {'brand': brand, 'name': name, 'price': findPrice(soup), 'image': findImageLink(soup), 
  'description': description, 'url': url, 'category' : category, 'key terms' : findKeyWords(description, name, brand), 
  'rec shirts' : [], 'rec pants' : [], 'rec shoes' : [], 'rec outer' : []}
  key = {'description' : description}
  products.update_one(key, {'$set' : product}, upsert=True)



menuesMen = [u'mens-tops', u'mens-tees-tanks-graphic', u'mens-jackets-and-coats', u'mens-bottom', u'mens-accessories', u'mens-shoes', u'branded-shop-men']

noPage = ["mens-jackets-and-coats", "mens-bottom", "mens-shoes"]

categoryMap = {'mens-tops' : 'Shirts', 'mens-tees-tanks-graphic' : 'Shirts', 'mens-bottom' : 'Pants & Shorts', 'mens-jackets-and-coats' : 'Jackets, Sweaters, & Outerwear', 
'mens-accessories' : 'Other', 'mens-shoes' : 'Shoes & Other Footwear', 'branded-shop-men' : 'Other'}

exceptionList = {'Tank' : 'Shirts','T-Shirt' : 'Shirts','Tee' : 'Shirts', 'Jeans' : 'Pants & Shorts', 'Sweatshirt' : 'Shirt', 'Joggers' : 'Pants & Shorts', 'Jogger' : 'Pants & Shorts','Hoodie' : 'Jackets, Sweaters, & Outerwear', 'Jacket' : 'Jackets, Sweaters, & Outerwear', 'Shirt': 'Shirts', 
'Pullover' : 'Jackets, Sweaters, & Outerwear', 'Kimono' : 'Jackets, Sweaters, & Outerwear', 'Sweatpants' : 'Pants & Shorts', 'Jersey' : 'Shirts', 'Jean' : 'Pants & Shorts', 'Pant' : 'Pants & Shorts', 
'Anorak' : 'Jackets, Sweaters, & Outerwear', 'Pancho' : 'Jackets, Sweaters, & Outerwear', 'Bomber' : 'Jackets, Sweaters, & Outerwear', 'Windbreaker' : 'Jackets, Sweaters, & Outerwear', 'Shorts' : 'Pants & Shorts'}

commonWords = ['the', 'in', 'and', 'with', 'for', 'on', 'this', 'that', 'an', 'it', 'anything', 'to', 'a', 'its', 'these', 'give', 'gives', 
'look', 'looks', 'like', 'of', 'any', 'but', 'where', 'when', 'wear', 'made', 'thanks', 'you', 'yours', 'your', 'is', 'as', 'just', 'from', 'our', 'at']

titleWords = []

for word in commonWords:
  titleWords.append(word.title())

commonWords = commonWords + titleWords


params = {"action": "getcategory",
          "br": "21men",
          "category": menuesMen[0],
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

while menuIndex < len(menuesMen):
  params["category"] = menuesMen[menuIndex]
  category = categoryMap[menuesMen[menuIndex]]
  print params["category"]
  params["pageno"] = 1
  js = requests.get(url, params=params).json()
  soup = BeautifulSoup(js[u'CategoryHTML'], "html.parser")
  while len(soup.select("div.item_pic a")) != 0:
    for a in soup.select("div.item_pic a"):
      postProduct(a["href"], category)
      i = i + 1
      j = j + 1
    if (params["category"] in noPage):
      break
    print params["pageno"]
    params["pageno"] = params["pageno"] + 1
    js = requests.get(url, params=params).json()
    soup = BeautifulSoup(js[u'CategoryHTML'], "html.parser")
  menuIndex = menuIndex + 1
  print i
  i = 0

print j
print "done"