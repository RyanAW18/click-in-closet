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

base_url = "http://www.jcrew.com"

urlTest = "https://www.jcrew.com/p/mens_category/shirts/secretwash/secret-wash-shirt-in-redandgreen-tartan-heather-poplin/F8040"
html = requests.get(urlTest)
soup = BeautifulSoup(html.text, "html.parser")

def findBrand(soup):
  return "JCrew"

def findPrice(soup):
  price = soup.find('span', class_='tile__detail tile__detail--price--list')
  print price
  if price is not None:
    return price.text

def findProductName(soup):
  product = soup.find('h1', class_='product__name')
  if product is not None:
    return product.text

def findImageLink(soup):
  image = soup.find('div', class_='product__image')
  return image
  # links = image.findAll('src')
  # for link in links:
  #   if link is not None:
  #     return link

def findDescription(soup):
  description = soup.find('p', {"class" : "intro"})
  if description is not None:
    return description.text

# def postProduct(url):
# 	html = urllib.urlopen(url).read()
# 	soup = BeautifulSoup(html, "html.parser")
# 	product = {'brand': findBrand(soup), 'name': findProductName(soup), 'price': findPrice(soup), 'image': findImageLink(soup), 'description': findDescription(soup), 'url': url}
# 	products.insert(product)

print findBrand(soup)
print findPrice(soup)
print findProductName(soup)
print findImageLink(soup)
print findDescription(soup)

# totalLinks = []
# j = 0

# # bigMenu = ["http://www.oldnavy.com/browse/division.do?cid=5360&mlink=5151,11140339,Top_nav_W&visnav=1&clink=11140339", "http://www.oldnavy.com/browse/division.do?cid=5585&mlink=5151,11140339,Top_nav_WP&visnav=1&clink=11140339",
# # "http://www.oldnavy.com/browse/division.do?cid=5758&mlink=5151,11140339,Top_nav_Mat&visnav=1&clink=11140339", "http://www.oldnavy.com/browse/division.do?cid=5360&mlink=5151,11140339,Top_nav_M&visnav=1&clink=11140339", 
# # "http://www.oldnavy.com/browse/division.do?cid=5360&mlink=5151,11140339,Top_nav_G&visnav=1&clink=11140339", "http://www.oldnavy.com/browse/division.do?cid=5360&mlink=5151,11140339,Top_nav_B&visnav=1&clink=11140339"]

# html = requests.get(base_url)
# soup = BeautifulSoup(html.text, "html.parser")
# categories = soup.findAll('div', {"class" : "menu__item"})
# for link in categories:
#   allLinks = link.findAll("a")
#   for a in allLinks:
#     totalLinks.append(a["href"])


# for link in totalLinks:
#   new_url = base_url + link
#   print new_url
#   html = requests.get(new_url)
#   soup = BeautifulSoup(html.text, "html.parser")
#   while len(soup.select("div.c-product-tile a")) != 0:
#     for a in soup.select("div.c-product-tile a"):
#       j = j + 1
#       productUrl = base_url + a["href"]
#       print productUrl
#       # postProduct(productUrl)
#     pageHtml = soup.find("div", class_= "category__pagination")
#     for div in pageHtml:
#       links = div.findAll('a')
#       nullLink = div.find('span', class_='pagination__link is-disabled')
#       for link in links:
#         if nullLink is not None:
#           break
#         pageUrl = link['href']
#     if nullLink is not None:
#       break
#     #need to fix the product urls. it will not work without it. go to pagination href for clarification
#     pageUrl = pageUrl.replace("..", "")
#     pageUrl = base_url + pageUrl
#     print j

# print j
# print "done"