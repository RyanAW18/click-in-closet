#Footlocker Crawler/Scraper


# import statements needed to create web crawler. Includes
# import statments for BeautifulSoup, Requests, URL libraries, and JSON
from bs4 import BeautifulSoup
import urllib
import urllib2
import requests
#import re

url = "http://www.footlocker.com/product/model:98963/sku:24300657/nike-air-force-1-low-mens/all-white/white/"
# html = urllib.urlopen(url).read()
html = requests.get(url)
# soup = BeautifulSoup(html, "html.parser")
soup = BeautifulSoup(html.text, "html.parser")


def retailerName(soup):
	print "Footlocker"

def priceTag(soup):
	price = soup.find('meta', {"itemprop" : "price"})
	if price is not None:
		print price["content"]

def productName(soup):
	product = soup.find('meta', property= "og:title")
	if product is not None:
		print product["content"]

# def brandName(soup):
# 	brand = soup.find('h1', class_='brand_name_p')
# 	print brand.text

def imageLink(soup):
	image = soup.find('meta', {"itemprop" : "og:image"})
	if image is not None:
		print image['content']

def description(soup):
	description = soup.find('span', {"itemprop" : "description"})
	if description is not None:
		print description.text

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