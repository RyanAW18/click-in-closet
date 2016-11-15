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

base_url = "http://www.ralphlauren.com"


def findBrand(soup):
  return "Ralph Lauren"

def findPrice(soup):
  price = soup.find('span', {"itemprop" : "price"})
  if price is not None:
    return price.text

def findProductName(soup):
  product = soup.find('h1', class_='prod-title')
  if product is not None:
    return product.text

def findImageLink(soup):
  image = soup.find('meta', {"property" : "og:image"})
  if image is not None:
    return image['content']

def findDescription(soup):
  description = soup.find('span', {"itemprop" : "description"})
  if description is not None:
    return description.text

def postProduct(url):
	html = urllib.urlopen(url).read()
	soup = BeautifulSoup(html, "html.parser")
	product = {'brand': findBrand(soup), 'name': findProductName(soup), 'price': findPrice(soup), 'image': findImageLink(soup), 'description': findDescription(soup), 'url': url}
	products.insert(product)



totalLinks = []
j = 0

bigMenu = ["http://www.ralphlauren.com/shop/index.jsp?categoryId=1760781&ab=global_men", "http://www.ralphlauren.com/shop/index.jsp?categoryId=1760782&ab=global_women",
"http://www.ralphlauren.com/shop/index.jsp?categoryId=105240616&ab=global_boys", "http://www.ralphlauren.com/shop/index.jsp?categoryId=105243666&ab=global_girls"]

for menu in bigMenu:
  html = requests.get(menu)
  soup = BeautifulSoup(html.text, "html.parser")
  categories = soup.findAll('li', {"onmouseover" : "this.className='leftnavlinkover'"})
  for link in categories:
    allLinks = link.findAll("a")
    for a in allLinks:
      varCheck = a["href"].split("/")
      if varCheck[1] == "family":
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
      postProduct(productUrl)
    pageHtml = soup.find("div", id= "pagination")
    for div in pageHtml:
      links = div.findAll('a')
      nullLink = div.find('span', class_='next-page-disabled')
      for link in links:
        if nullLink is not None:
          break
        pageUrl = link['href']
    if nullLink is not None:
      break
    pageUrl = pageUrl.replace("..", "")
    pageUrl = base_url + pageUrl
    print j
    html = requests.get(pageUrl)
    soup = BeautifulSoup(html.text, "html.parser")

print j
print "done"