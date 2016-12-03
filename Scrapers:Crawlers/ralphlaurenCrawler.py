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


base_url = "http://www.ralphlauren.com"


def findBrand(soup):
  return "Ralph Lauren"

def findPrice(soup):
  price = soup.find('span', {"itemprop" : "price"})
  if price is not None:
    return price.text

def findProductName(soup):
  product = soup.find('div', {'itemprop' : 'name'})
  productName = product.find('h1')
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

def findKeyWords(description, name, brand):
  keyTerms = []
  superString = description + ' ' + name + ' ' + brand
  terms = superString.split(' ')
  for term in terms:
    if term not in commonWords:
      keyTerms.append(term)
  return keyTerms

def postProduct(url, category):
  html = urllib.urlopen(url).read()
  soup = BeautifulSoup(html, "html.parser")
  name = findProductName(soup)
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


apparelCategories = {}
accessoryLinks = []

menUrl = "http://www.ralphlauren.com/shop/index.jsp?categoryId=1760781&ab=global_men"
html = requests.get(menUrl)
soup = BeautifulSoup(html.text, "html.parser")

nav = soup.find('div', class_= "nav")
lists = nav.findAll('ul')

print "got lists"

apparel = lists[0]
apparelList = apparel.findAll('li')
i = 1
while i < len(apparelList) - 1:
  apparelLink = apparelList[i].find('a')["href"]
  apparelText = apparelList[i].find('a').text
  apparelCategories[apparelText] = apparelLink
  i = i + 1

print "got apparel"

accessories = lists[3]
accessoriesList = accessories.findAll('li')
i = 1
while i < len(accessoriesList) - 1:
  accessoryLink = accessoriesList[i].find('a')["href"]
  accessoryLinks.append(accessoryLink)
  i = i + 1

print "got accessories"


shoesAll = lists[2]
shoes = shoesAll.findAll('li')
shoesLink = shoes[0].find('a')["href"]

print "got shoes"


apparelCategoryMap = {'Polo Shirts' : 'Shirts', 'T-Shirts & Sweatshirts' : 'Shirts', 'Casual Shirts' : 'Shirts', 'Sweaters' : 'Jackets, Sweaters, & Outerwear', 
'Pants & Jeans' : 'Pants & Shorts', 'Dress Shirts' : 'Shirts', 'Suits, Sport Coats & Trousers' : 'Jackets, Sweaters, & Outerwear', 
'Shorts & Swim' : 'Pants & Shorts', 'Underwear & Sleepwear' : 'Other'}

exceptionList = {'Hoodie' : 'Jackets, Sweaters, & Outerwear', 'Jacket' : 'Jackets, Sweaters, & Outerwear', 'Sweater': 'Jackets, Sweaters, & Outerwear', 
'Pullover' : 'Jackets, Sweaters, & Outerwear', 'Swim' : 'Other', 'Trunk' : 'Other', 'Trouser' : 'Pants & Shorts', 'Suits' : 'Other'}

commonWords = ['the', 'in', 'and', 'with', 'for', 'on', 'this', 'that', 'an', 'it', 'anything', 'to', 'a', 'its', 'these', 'give', 'gives', 
'look', 'looks', 'like', 'of', 'any', 'but', 'where', 'when', 'wear', 'made', 'thanks', 'you', 'yours', 'your', 'is', 'as', 'just', 'from', 'our']

titleWords = []

for word in commonWords:
  titleWords.append(word.title())

commonWords = commonWords + titleWords

print 'Starting'

j = 0

for key in apparelCategories:
  category = apparelCategoryMap[key]
  categoryLink = apparelCategories[key]
  new_url = base_url + categoryLink
  html = requests.get(new_url)
  soup = BeautifulSoup(html.text, "html.parser")
  while len(soup.select("div.product-photo a")) != 0:
    for a in soup.select("div.product-photo a"):
      j = j + 1
      productUrl = base_url + a["href"]
      postProduct(productUrl, category)
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
    html = requests.get(pageUrl)
    soup = BeautifulSoup(html.text, "html.parser")

print "apparel total: " +  j

k = 0

for link in accessoryLinks:
  new_url = base_url + link
  html = requests.get(new_url)
  soup = BeautifulSoup(html.text, "html.parser")
  while len(soup.select("div.product-photo a")) != 0:
    for a in soup.select("div.product-photo a"):
      k = k + 1
      productUrl = base_url + a["href"]
      postProduct(productUrl, 'Other')
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
    html = requests.get(pageUrl)
    soup = BeautifulSoup(html.text, "html.parser")

print "accessory total: " +  k



m = 0

new_url = base_url + shoesLink
html = requests.get(new_url)
soup = BeautifulSoup(html.text, "html.parser")
while len(soup.select("div.product-photo a")) != 0:
  for a in soup.select("div.product-photo a"):
    m = m + 1
    productUrl = base_url + a["href"]
    postProduct(productUrl, 'Shoes & Other Footwear')
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
  html = requests.get(pageUrl)
  soup = BeautifulSoup(html.text, "html.parser")

print "shoe total: " + m

print "done, product total : " + (j + k + m)