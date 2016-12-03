from bs4 import BeautifulSoup
from selenium import webdriver
import time
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

urlTest = "http://oldnavy.gap.com/browse/product.do?cid=1036301&vid=1&pid=334144082"
driver = webdriver.PhantomJS()
driver.get(urlTest)
html = driver.page_source
soup = BeautifulSoup(html, "html.parser")


def findBrand(soup):
  return "Old Navy"

def findPrice(soup):
  price = soup.find('h5', class_='product-price')
  highlight = soup.find('span', class_='product-price--highlight')
  if price is not None:
    if highlight is not None:
      priceTag = highlight.text.strip()
    else:
      priceTag = price.contents[0].strip()
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

def postProduct(url):
  print "product url: " + url
  driver = webdriver.PhantomJS()
  driver.get(url)
  html = driver.page_source
  soup = BeautifulSoup(html, "html.parser")
  product = {'brand': findBrand(soup), 'name': findProductName(soup), 'price': findPrice(soup), 'image': findImageLink(soup), 'description': findDescription(soup), 'url': url}
  products.insert(product)

print findBrand(soup)
print findPrice(soup)
print findProductName(soup)
print findImageLink(soup)
print findDescription(soup)


# totalLinks = []
# linkTotal = 0
# j = 0
# nextText = ""

# bigMenu = ["http://www.oldnavy.com/browse/division.do?cid=5360&mlink=5151,11140339,Top_nav_W&visnav=1&clink=11140339", "http://www.oldnavy.com/browse/division.do?cid=5585&mlink=5151,11140339,Top_nav_WP&visnav=1&clink=11140339",
# "http://www.oldnavy.com/browse/division.do?cid=5758&mlink=5151,11140339,Top_nav_Mat&visnav=1&clink=11140339", "http://oldnavy.gap.com/browse/division.do?cid=5155&mlink=5151,11140339,Top_nav_M&visnav=1&clink=11140339", 
# "http://oldnavy.gap.com/browse/division.do?cid=6027&mlink=5151,11140339,Top_nav_G&visnav=1&clink=11140339", "http://oldnavy.gap.com/browse/division.do?cid=5910&mlink=5151,11140339,Top_nav_B&visnav=1&clink=11140339"]

# for menu in bigMenu:
#   driver = webdriver.PhantomJS()
#   driver.get(menu)
#   html = driver.page_source
#   soup = BeautifulSoup(html, "html.parser")
#   print "new page"
#   headers = soup.findAll("span", class_="sidebar-navigation--header--text")
#   for head in headers:
#     if head.text.strip() == "Shop by Category":
#       parent = head.findParent("h2")
#       newlist = parent.findAllNext("div", class_="sidebar-navigation--item sidebar-navigation--category")
#       for item in newlist:
#         # new addition
#         links = item.findAll("a")
#         for i in links:
#           linkTotal = linkTotal + 1
#           varCheck = i["href"].split("/")
#           if varCheck[1] == "browse":
#             if base_url + i["href"] not in totalLinks:
#               totalLinks.append(base_url + i["href"])
#           else:
#             if i["href"] not in totalLinks:
#               totalLinks.append(i["href"])
#         itemNext = item.findNextSibling()
#         nextHeadSpan = itemNext.find("span", class_="sidebar-navigation--header--text")
#         if nextHeadSpan is not None:
#           print "head span found"
#           nextText = nextHeadSpan.text.strip()
#           if nextText == "Deals":
#             print "oops: " + nextText
#             break
#       if nextText == "Deals":
#         break

# for link in totalLinks:
#   print "link: " + link
#   driver = webdriver.PhantomJS()
#   driver.get(link)
#   # lazy loading method for scrolling
#   lastHeight = driver.execute_script("return document.body.scrollHeight")
#   pause = 0.5

#   while True:
#     driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
#     time.sleep(pause)
#     newHeight = driver.execute_script("return document.body.scrollHeight")
#     if newHeight == lastHeight:
#         break
#     lastHeight = newHeight

#   # end of lazy scrolling method
#   html = driver.page_source
#   soup = BeautifulSoup(html, "html.parser")
#   bigDiv = soup.findAll("div", class_="sp_sm spacing_small")
#   for div in bigDiv:
#     links = div.findAll("a")
#     for i in links:
#       j = j + 1
#       productUrl = base_url + i["href"]
#       postProduct(productUrl)
#     print j

# print j
# print "done"