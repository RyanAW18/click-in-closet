from bs4 import BeautifulSoup
from selenium import webdriver
import platform
import urllib
import urllib2
import requests
import json

from pymongo import MongoClient
client = MongoClient('mongodb://trossi:1460@ds143707.mlab.com:43707/heroku_b37frt6h')
db = client.heroku_b37frt6h
products = db.products
products.create_index([("name", "text"), ("brand", "text")])

base_url = "http://www.urbanoutfitters.com"

def findBrand(soup):
  return "Urban Outfitters"

def findPrice(soup):
  price = soup.find('h1', class_="product-price")
  priceTag = price.find('span', {"class" : "mainPrice ng-scope ng-binding"})
  if priceTag is not None:
    return priceTag.text.strip()

def findProductName(soup):
  product = soup.find('h1', class_='ng-scope ng-isolate-scope ng-binding')
  if product is not None:
    return product.text

def findImageLink(soup):
  image = soup.find('meta', {"property" : "og:image"})
  if image is not None:
    return image['content']

def findDescription(soup):
  description = soup.find('div', class_="product-description child")
  deepDescription = description.find('div', class_="ng-binding")
  paragraph = deepDescription.find('p')
  if paragraph.text is not None:
    return paragraph.text

def postProduct(url):
	html = urllib.urlopen(url).read()
	soup = BeautifulSoup(html, "html.parser")
	product = {'brand': findBrand(soup), 'name': findProductName(soup), 'price': findPrice(soup), 'image': findImageLink(soup), 'description': findDescription(soup), 'url': url}
	products.insert(product)



totalLinks = []
j = 0


categories_url = "http://www.urbanoutfitters.com/urban/catalog/category.jsp?id=WOMENS&cm_sp=WOMENS-_-L1-_-WOMENS:WOMENS"

driver = webdriver.PhantomJS()
driver.get(categories_url)
html = driver.page_source
soup = BeautifulSoup(html, "html.parser")
men = soup.find('div', {"data-nav" : "mens"})
women = soup.find('div', {"data-nav" : "womens"})
menCategories = men.findAll('div', class_= "subnavColWrapper")
womenCategories = women.findAll('div', class_= "subnavColWrapper")
for link in womenCategories:
  mainCat = link.findAll("p")
  for p in mainCat:
    allLinks = p.findAll("a")
    for a in allLinks:
      new_url = base_url + a["href"]
      totalLinks.append(new_url)
for link in menCategories:
  mainCat = link.findAll("p")
  for p in mainCat:
    allLinks = p.findAll("a")
    for a in allLinks:
      new_url = base_url + a["href"]
      totalLinks.append(new_url)

catalog_base_url = "http://www.urbanoutfitters.com/urban/catalog/"
nextPage_url = "http://www.urbanoutfitters.com/urban/catalog/category.jsp"
nullLink = False

testUrl = "http://www.urbanoutfitters.com/urban/catalog/category.jsp?id=W_APP_DRESSES&cm_sp=WOMENS-_-L2-_-WOMENS:W_APP_DRESSES"

for link in totalLinks:
  print link
  driver.get(link)
  html = driver.page_source
  soup = BeautifulSoup(html, "html.parser")
  while len(soup.select("div.media a")) != 0:
    for a in soup.select("div.media a"):
      j = j + 1
      productUrl = catalog_base_url + a["href"]
      postProduct(productUrl)
    pageHtml = soup.findAll("div", class_= "pagination")
    for div in pageHtml:
      link = div.find('a', class_="icon icon-RightArrow")
      if link is None:
        print "uh oh no next page"
        nullLink = None
        break
      pageUrl = link['href']
    if nullLink is None:
      nullLink = False
      break
    pageUrl = nextPage_url + pageUrl
    print j
    print "new page link: " + pageUrl
    driver.get(pageUrl)
    html = driver.page_source
    soup = BeautifulSoup(html, "html.parser")

print j
print "done"