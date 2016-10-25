#JCrew Crawler/Scraper


# import statements needed to create web crawler. Includes
# import statments for BeautifulSoup, Requests, URL libraries, and JSON
from bs4 import BeautifulSoup
import urllib
import urllib2
#import re

url = "https://www.jcrew.com/mens_category/shirts/secretwash/PRDOVR~F4086/F4086.jsp?color_name=hthr-oatmeal-grey"
html = urllib.urlopen(url).read()
soup = BeautifulSoup(html, "html.parser")


def retailerName(soup):
	print "JCrew"

def priceTag(soup):
	priceArray = soup.findAll('span', {"itemprop" : "price"})
	if priceArray is not None:
		for price in priceArray:
			print price.text

def productName(soup):
	product = soup.find('h1', class_='item_name_p')
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