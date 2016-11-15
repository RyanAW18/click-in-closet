from bs4 import BeautifulSoup
import urllib
import urllib2
import requests
import json

from pymongo import MongoClient
client = MongoClient('mongodb://trossi:1460@ds143707.mlab.com:43707/heroku_b37frt6h')
db = client.heroku_b37frt6h
products = db.products
products.create_index([("name", "text"), ("brand", "text")])

base_url = "http://www.oldnavy.com"


def findBrand(soup):
  return "Old Navy"

def findPrice(soup):
  price = soup.find('h5', class_='product-price')
  if price is not None:
    return price.text

def findProductName(soup):
  product = soup.find('h1', class_='product-title')
  if product is not None:
    return product.text

def findImageLink(soup):
  image = soup.find('div', class_='product-photo')
  links = image.findAll('a')
  for link in links:
    if link["href"] is not None:
      otherUrl = base_url + link["href"]
      return otherUrl

# def findDescription(soup):
#   description = soup.find('span', {"itemprop" : "description"})
#   if description is not None:
#     return description.text

def postProduct(url):
	html = urllib.urlopen(url).read()
	soup = BeautifulSoup(html, "html.parser")
	product = {'brand': findBrand(soup), 'name': findProductName(soup), 'price': findPrice(soup), 'image': findImageLink(soup), 'description': findDescription(soup), 'url': url}
	products.insert(product)



totalLinks = []
j = 0

bigMenu = ["http://www.oldnavy.com/browse/division.do?cid=5360&mlink=5151,11140339,Top_nav_W&visnav=1&clink=11140339", "http://www.oldnavy.com/browse/division.do?cid=5585&mlink=5151,11140339,Top_nav_WP&visnav=1&clink=11140339",
"http://www.oldnavy.com/browse/division.do?cid=5758&mlink=5151,11140339,Top_nav_Mat&visnav=1&clink=11140339", "http://www.oldnavy.com/browse/division.do?cid=5360&mlink=5151,11140339,Top_nav_M&visnav=1&clink=11140339", 
"http://www.oldnavy.com/browse/division.do?cid=5360&mlink=5151,11140339,Top_nav_G&visnav=1&clink=11140339", "http://www.oldnavy.com/browse/division.do?cid=5360&mlink=5151,11140339,Top_nav_B&visnav=1&clink=11140339"]

for menu in bigMenu:
  html = requests.get(menu)
  soup = BeautifulSoup(html.text, "html.parser")
  categories = soup.findAll('div', {"class" : "sidebar-navigation--item sidebar-navigation--category"})
  for link in categories:
    allLinks = link.findAll("a")
    for a in allLinks:
      totalLinks.append(a["href"])

for link in totalLinks:
  new_url = base_url + link
  print new_url
  html = requests.get(new_url)
  soup = BeautifulSoup(html.text, "html.parser")
  while len(soup.select("div.product-photo a")) != 0:
    for a in soup.select("div.product-photo a"):
      j = j + 1
      productUrl = base_url + a["href"]
      print productUrl
      # postProduct(productUrl)
    print j

print j
print "done"