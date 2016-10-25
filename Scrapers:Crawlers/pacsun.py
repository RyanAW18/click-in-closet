#PacSun Crawler/Scraper


# import statements needed to create web crawler. Includes
# import statments for BeautifulSoup, Requests, URL libraries, and JSON
from bs4 import BeautifulSoup
import urllib
import urllib2
#import re

url = "http://www.pacsun.com/sublime-tie-dye-t-shirt-0097112540021.html?cgid=mens&start=2&dwvar_0097112540021_color=998"
html = urllib.urlopen(url).read()
soup = BeautifulSoup(html, "html.parser")


def retailerName(soup):
	print "PacSun"


# weird issue with price tag
def priceTag(soup):
	price = soup.find('div', class_= 'standardprice')
	print price
	if price is not None:
		print price.text

def productName(soup):
	product = soup.find('h1')
	if product is not None:
		print product.text

# def brandName(soup):
# 	brand = soup.find('h1', class_='brand_name_p')
# 	print brand.text

def imageLink(soup):
	image = soup.find('meta', {"property" : "og:image"})
	if image is not None:
		print image['content']

def description(soup):
	description = soup.find('meta', {"property" : "og:description"})
	if description is not None:
		print description['content']

def printUrl(soup):
	url = soup.find('meta', {"property" : "og:url"})
	if url is not None:
		print url['content']

# brandName(soup)
retailerName(soup)
priceTag(soup)
productName(soup)
imageLink(soup)
description(soup)
printUrl(soup)