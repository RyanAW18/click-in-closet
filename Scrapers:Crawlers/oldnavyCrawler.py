from bs4 import BeautifulSoup
from selenium import webdriver
import html5lib
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

base_url = "http://www.oldnavy.com"

# driver = webdriver.PhantomJS()

# driver.get("http://oldnavy.gap.com/browse/product.do?cid=84470&vid=1&pid=275038022")

# html = driver.page_source

# driver.close()

# soup = BeautifulSoup(html, "html.parser")

def findBrand(soup):
  return "Old Navy"

def findPrice(soup):
  price = soup.find('span', class_='product-price--highlight')
  if price is not None:
    priceTag = price.text.strip()
    return priceTag

def findProductName(soup):
  product = soup.find('h1', class_='product-title')
  if product is not None:
    productName = product.text.strip()
    return productName

# not giving src link for the image
def findImageLink(soup):
  image = soup.find('img', class_="product-photo--image")
  links = image['src']
  return links

def findDescription(soup):
  description = soup.findAll("ul", class_="sp_top_sm dash-list")[1]
  if description is not None:
    return description.text.strip()
  else:
    return "No description available for this item"

# def postProduct(url):
# 	html = urllib.urlopen(url).read()
# 	soup = BeautifulSoup(html, "html.parser")
# 	product = {'brand': findBrand(soup), 'name': findProductName(soup), 'price': findPrice(soup), 'image': findImageLink(soup), 'description': findDescription(soup), 'url': url}
# 	products.insert(product)

# print findBrand(soup)
# print findPrice(soup)
# print findProductName(soup)
# print findImageLink(soup)
# print findDescription(soup)


totalLinks = []
linkTotal = 0
j = 0
nextText = ""

bigMenu = ["http://www.oldnavy.com/browse/division.do?cid=5360&mlink=5151,11140339,Top_nav_W&visnav=1&clink=11140339", "http://www.oldnavy.com/browse/division.do?cid=5585&mlink=5151,11140339,Top_nav_WP&visnav=1&clink=11140339",
"http://www.oldnavy.com/browse/division.do?cid=5758&mlink=5151,11140339,Top_nav_Mat&visnav=1&clink=11140339", "http://www.oldnavy.com/browse/division.do?cid=5360&mlink=5151,11140339,Top_nav_M&visnav=1&clink=11140339", 
"http://www.oldnavy.com/browse/division.do?cid=5360&mlink=5151,11140339,Top_nav_G&visnav=1&clink=11140339", "http://www.oldnavy.com/browse/division.do?cid=5360&mlink=5151,11140339,Top_nav_B&visnav=1&clink=11140339"]

for menu in bigMenu:
  driver = webdriver.PhantomJS()
  driver.get(menu)
  html = driver.page_source
  soup = BeautifulSoup(html, "html.parser")
  print "new page"
  headers = soup.findAll("span", class_="sidebar-navigation--header--text")
  for head in headers:
    if head.text.strip() == "Shop by Category":
      parent = head.findParent("h2")
      newlist = parent.findAllNext("div", class_="sidebar-navigation--item sidebar-navigation--category")
      for item in newlist:
        # new addition
        links = item.findAll("a")
        for i in links:
          linkTotal = linkTotal + 1
          totalLinks.append(i["href"])
        itemNext = item.findNextSibling()
        nextHeadSpan = itemNext.find("span", class_="sidebar-navigation--header--text")
        if nextHeadSpan is not None:
          print "head span found"
          nextText = nextHeadSpan.text.strip()
          if nextText == "Deals":
            print "oops: " + nextText
            break
      if nextText == "Deals":
        break

print "got links"
print linkTotal

#ERROR SPOT!
#issues with accessing all of the products on the page
for link in totalLinks:
  print "link: " + link
  driver = webdriver.PhantomJS()
  driver.get(link)
  html = driver.page_source
  soup = BeautifulSoup(html, "html5lib")
  bigDiv = soup.findAll("div", class_="sp_sm spacing_small")
  for div in bigDiv:
    links = div.findAll("a")
    for i in links:
      j = j + 1
      productUrl = base_url + i["href"]
      print productUrl
        # print productUrl
        # postProduct(productUrl)
    print j

print j
print "done"