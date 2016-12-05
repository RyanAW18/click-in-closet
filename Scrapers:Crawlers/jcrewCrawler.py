from bs4 import BeautifulSoup
from selenium import webdriver
import urllib
import urllib2
import requests
import json
import commonwords

from pymongo import MongoClient
client = MongoClient('mongodb://trossi:1460@ds143707.mlab.com:43707/heroku_b37frt6h')
db = client.heroku_b37frt6h
products = db.productsMen
products.create_index([("name", "text"), ("brand", "text")])

base_url = "http://www.jcrew.com"

urlTest = "https://www.jcrew.com/mens_category/dressshirts/cordings/PRDOVR~E2464/E2464.jsp"
# html = requests.get(urlTest)
# soup = BeautifulSoup(html.text, "html.parser")


def findBrand(soup):
  return "J.Crew"

def findPrice(soup):
  priceTag = soup.find('div', class_='full-price')
  if priceTag is None:
    return None
  price = priceTag.find('span')
  if price is not None:
    return price.text
  else:
    price = soup.find('span', class_="full-price")
    if price is not None:
      return price.text


def findProductName(soup):
  product = soup.find('h1', {'itemprop' : "name"})
  if product is not None:
    return product.text
  else:
    return None

def findImageLink(soup):
  image = soup.find('img', class_='prod-main-image')
  if image is not None:
    return image['src']

def findDescription(soup):
  description = soup.find('div', class_= "product_desc")
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
  print "url: " + url
  driver.get(url)
  html = driver.page_source
  soup = BeautifulSoup(html, "html.parser")
  brand = findBrand(soup)
  name = findProductName(soup)
  if name is None:
    print "NAME FAIL!!!!!!!!!!"
    return 1
  print "name: " + name
  price = findPrice(soup)
  if price is None:
    print "PRICE FAIL!!!!!!!!!!"
    return 1
  image = findImageLink(soup)
  if image is None:
    print "IMAGE FAIL!!!!!!!!!!"
    return 1
  description = findDescription(soup)
  # if description is None:
  #   return
  nameTerms = name.split(' ')
  for term in nameTerms:
    if term in exceptionList:
      category = exceptionList[term]
  product = {'brand': brand, 'name': name, 'price': findPrice(soup), 'image': findImageLink(soup), 
  'description': description, 'url': url, 'category' : category, 'key terms' : findKeyWords(description, name, brand), 
  'rec shirts' : [], 'rec pants' : [], 'rec shoes' : [], 'rec outer' : []}
  key = {'description' : description}
  products.update_one(key, {'$set' : product}, upsert=True)
  # print product


# driver = webdriver.PhantomJS()
# driver.get(urlTest)
# html = driver.page_source
# soup = BeautifulSoup(html, "html.parser")


# ret = postProduct(urlTest, "Shirts")
# print "done"





totalLinks = []
j = 0


apparelCategories = {}
accessoryLinks = []

menUrl = "https://www.jcrew.com/mens-clothing.jsp"
driver = webdriver.PhantomJS()
driver.get(menUrl)
html = driver.page_source
soup = BeautifulSoup(html, "html.parser")

nav = soup.find('div', class_= "leftnav leftnav")
lists = nav.findAll('ul', class_= "leftnav_sub")

apparel = lists[1]
apparelList = apparel.findAll('li')
i = 0
while i < len(apparelList):
  apparelLink = apparelList[i].find('a')
  hyperlink = apparelLink["href"]
  apparelText = apparelLink.text
  apparelCategories[apparelText] = hyperlink
  i = i + 1

shoes_accessories = lists[2]
shoes_accessoriesList = shoes_accessories.findAll('li')
shoesLink = None
i = 0
while i < len(shoes_accessoriesList):
  otherLink = shoes_accessoriesList[i].find('a')
  hyperlink = otherLink["href"]
  if i == 0:
    shoesLink = hyperlink
  else:
    accessoryLinks.append(hyperlink)
  i = i + 1


apparelCategoryMap = {'casual shirts' : 'Shirts', 'dress shirts' : 'Shirts', 't-shirts & polos' : 'Shirts', 'sweaters' : 'Jackets, Sweaters, & Outerwear', 
'sweatshirts & sweatpants' : 'Shirts', 'coats & jackets' : 'Jackets, Sweaters, & Outerwear','blazers & vests' : 'Jackets, Sweaters, & Outerwear',
'suits' : 'Other','Casual Pants' : 'Pants & Shorts','Dress Pants' : 'Pants & Shorts', 'Denim' : 'Pants & Shorts', 'shorts' : 'Pants & Shorts',
'swim' : 'Other','underwear & pajamas' : 'Other', 'wallace & barnes' : 'Other', 'j.crew in good company' : 'Other', 
'Thomas Mason' : 'Other'}

exceptionList = {'Tank' : 'Shirts','T-Shirt' : 'Shirts','Tee' : 'Shirts', 'Jeans' : 'Pants & Shorts', 'Sweatshirt' : 'Shirts', 'Joggers' : 'Pants & Shorts', 'Jogger' : 'Pants & Shorts','Hoodie' : 'Jackets, Sweaters, & Outerwear', 'Jacket' : 'Jackets, Sweaters, & Outerwear', 'Shirt': 'Shirts', 
'Pullover' : 'Jackets, Sweaters, & Outerwear', 'Kimono' : 'Jackets, Sweaters, & Outerwear', 'Sweatpants' : 'Pants & Shorts', 'Jersey' : 'Shirts', 'Jean' : 'Pants & Shorts', 'Pant' : 'Pants & Shorts', 
'Anorak' : 'Jackets, Sweaters, & Outerwear', 'Pancho' : 'Jackets, Sweaters, & Outerwear', 'Bomber' : 'Jackets, Sweaters, & Outerwear', 'Windbreaker' : 'Jackets, Sweaters, & Outerwear', 'Shorts' : 'Pants & Shorts', 'Flannel' : 'Shirts', 'Workshirt' : 'Shirts', 'Turtleneck' : 'Shirts', 
'Henley' : 'Jackets, Sweaters, & Outerwear', 'Cardigan' : 'Jackets, Sweaters, & Outerwear', 'Chino' : 'Pants & Shorts', 'Sneakers' : 'Shoes & Other Footwear', 'Oxfords' : 'Shoes & Other Footwear', 'Bluchers' : 'Shoes & Other Footwear', 'Boots' : 'Shoes & Other Footwear', 'Boot' : 'Shoes & Other Footwear',
'Brogues' : 'Shoes & Other Footwear', 'Slippers' : 'Shoes & Other Footwear', 'Slipper' : 'Shoes & Other Footwear', 'Sandals' : 'Shoes & Other Footwear', 'Sandal' : 'Shoes & Other Footwear', 'Short' : 'Pants & Shorts', 'Coat' : 'Jackets, Sweaters, & Outerwear', 'Topcoat' : 'Jackets, Sweaters, & Outerwear',
'Flip-flops' : 'Shoes & Other Footwear', 'Parka' : 'Jackets, Sweaters, & Outerwear', 'Sweatpant' : 'Pants & Shorts'}

exceptionTerms = exceptionList.keys()

for term in exceptionTerms:
  val = exceptionList[term]
  termLower = term.lower()
  exceptionList[termLower] = val


commonWords = commonwords.getCommonWords()


print 'Starting'
failCount = 0

j = 0

for key in apparelCategories:
  print "category: " + key
  category = apparelCategoryMap[key]
  categoryLink = apparelCategories[key]
  previousLink = categoryLink
  # new_url = base_url + categoryLink
  driver.get(categoryLink)
  html = driver.page_source
  soup = BeautifulSoup(html, "html.parser")
  while len(soup.select("a.product-image-wrap")) != 0:
    for a in soup.select("a.product-image-wrap"):
      j = j + 1
      productUrl = a["href"]
      ret = postProduct(productUrl, category)
      if ret is not None:
        failCount = failCount + ret
        print "fail: " + str(failCount)
        print "total: " + str(j)
    pageHtml = soup.find("div", class_= "paginationTop")
    if pageHtml is None:
      break
    else:
      nextLink = pageHtml.find('li', class_= 'pageNext')
      nullLink = nextLink.find('span', class_='disabled')
      if nullLink is not None:
        print "no next page"
        break
      hyperlink = nextLink.find('a')["href"]
    pageUrl = categoryLink + hyperlink
    if pageUrl == previousLink:
      break
    previousLink = pageUrl
    driver.get(pageUrl)
    html = driver.page_source
    soup = BeautifulSoup(html, "html.parser")
    print "new page"

print "apparel total: " + str(j)

k = 0

for link in accessoryLinks:
  print "category: " + link
  category = "Other"
  # new_url = base_url + categoryLink
  driver.get(link)
  html = driver.page_source
  soup = BeautifulSoup(html, "html.parser")
  while len(soup.select("a.product-image-wrap")) != 0:
    for a in soup.select("a.product-image-wrap"):
      k = k + 1
      productUrl = a["href"]
      ret = postProduct(productUrl, category)
      if ret is not None:
        failCount = failCount + ret
        print "fail: " + str(failCount)
        print "total: " + str(k)
    pageHtml = soup.find("div", class_= "paginationTop")
    if pageHtml is None:
      break
    else:
      nextLink = pageHtml.find('li', class_= 'pageNext')
      nullLink = nextLink.find('span', class_='disabled')
      if nullLink is not None:
        print "no next page"
        break
      hyperLink = ""
      hyperlink = nextLink.find('a')["href"]
    pageUrl = link + hyperlink
    driver.get(pageUrl)
    html = driver.page_source
    soup = BeautifulSoup(html, "html.parser")
    print "new page"

print "accessory total: " + str(k)

m = 0

category = "Shoes & Other Footwear"
# new_url = base_url + categoryLink
driver.get(shoesLink)
html = driver.page_source
soup = BeautifulSoup(html, "html.parser")
while len(soup.select("a.product-image-wrap")) != 0:
  for a in soup.select("a.product-image-wrap"):
    m = m + 1
    productUrl = a["href"]
    ret = postProduct(productUrl, category)
    if ret is not None:
      failCount = failCount + ret
      print "fail: " + str(failCount)
      print "total: " + str(m)
  pageHtml = soup.find("div", class_= "paginationTop")
  if pageHtml is None:
      break
  else:
    nextLink = pageHtml.find('li', class_= 'pageNext')
    nullLink = nextLink.find('span', class_='disabled')
    if nullLink is not None:
      print "no next page"
      break
    hyperLink = ""
    hyperlink = nextLink.find('a')["href"]
  pageUrl = shoesLink + hyperlink
  driver.get(pageUrl)
  html = driver.page_source
  soup = BeautifulSoup(html, "html.parser")
  print "new page"

print "shoe total: " + str(m)

tot = j + k + m

print "done, product total : " + str(tot)
print "fail count: " + str(failCount)