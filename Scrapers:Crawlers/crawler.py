from bs4 import BeautifulSoup
import urllib2
import urllib
import requests 
import json 
#import mysql.connector
#import boto

#from pymongo import MongoClient
#client = MongoClient('mongodb://francesca:harrison@kahana.mongohq.com:10025/gilt')
#db = client.gilt
#products2 = db.products2
class ProductParser: 
	def __init__(self, findImageLink, findProductName, findBrand, findPrice, findDescription, findUrl):
		self.findImage = findImageLink
		self.findProductName = findProductName
		self.findBrand = findBrand
		self.findPrice =findPrice 
		self.findDescription = findDescription
		self.findUrl = findUrl
		#self.checkBrand = False


	#def postProduct(self):
		#db = client.gilt
		#test2 = db.test2
		#newP = {'image': self.image, 'name': self.productName, 'brand': self.brand, 'purchaseUrl': self.purchaseUrl, 'price': self.price}
		#print newP
		#products2.insert(newP)
		
	def parse(self, soup, url):
		self.image = self.findImageLink(soup);
		self.productName = self.findProductName(soup);
		self.brand = self.findBrand(soup);
		self.price = self.findPrice(soup);
		self.description = self.findDescription(soup);
		self.url = self.findUrl(soup);
		print self.image
		print self.productName
		print self.brand
		print self.price
		print self.description
		print self.url
		print "-------------------------------------------------------"
		
		
class Parser:
	def __init__(self, productParser, findProductURLs):
		self.findProductURLs = findProductURLs
		self.productParser = productParser
		
		
	def parse(self, soup, url):
		print "Parsing soup at url", url
		urls = self.findProductURLs(soup, url);
		for url in urls:
			sock = urllib2.urlopen(url)
			print "Parsing product url: ", url
			try:
				product_soup = BeautifulSoup(sock.read().decode('utf-8'), "html.parser")
				self.productParser.parse(product_soup, url)
			except BaseException, e:
				print "Error:", str(e)
				print "Skipping product at url:", url
				continue
		
	

class Crawler:
	def __init__(self, entries, soupParser):
		self.entries = entries
		self.soupParser = soupParser

	def crawl(self):
		
		for url in self.entries:

			sock = urllib2.urlopen(url)
			#try:
			soup = BeautifulSoup(sock, "html.parser")
			self.soupParser.parse(soup, url)
			#except:
				#print "Testing category url: ", url
				#try:
				#	sock = BeautifulSoup(requests.get(url).text)
				#	self.soupParser.parse(soup,url)
				#except:
				#	print "real deal error"
			#continue

				
	
def removeSymbols(string):
	string = string.strip(u'\u00ae')
	string = string.strip(u'\r\n\t\t\t\t\t\t\t\t\t\t')
	string = string.strip(u'\xa0\xa0\xa0\xa0\xa0')
	string = string.strip(u'\u2122')
	string = string.strip(u'\u00a9')
	return string