from bs4 import BeautifulSoup
import urllib
import urllib2
import requests
#import sys
#from urlparse import urljoin
#import lxml
#sys.path.append("/Users/fcolombo/Documents/gilt");

#import defaultparser
import crawler
#import selenium.webdriver as webdriver



class ForeverCrawler:

	def getProductParser(self):
		def findBrand(soup):
			return "Forever21"

		def findPrice(soup):
			priceArray = soup.findAll('span', {"itemprop" : "price"})
			if priceArray is not None:
				for price in priceArray:
					return price.text
			return ""

		def findProductName(soup):
			product = soup.find('h1', class_='item_name_p')
			if product is not None:
				return product.text
			return ""

		def findImageLink(soup):
			image = soup.find('meta', {"property" : "og:image"})
			if image is not None:
				return image['content']
			return ""

		def findDescription(soup):
			description = soup.find('meta', {"property" : "og:description"})
			if description is not None:
				return description['content']
			return ""

		def findUrl(soup):
			url = soup.find('meta', {"property" : "og:url"})
			if url is not None:
				return url['content']
			return ""

		productParser = crawler.ProductParser(findImageLink, findProductName, findBrand, findPrice, findDescription, findUrl)
		productParser.findBrand = findBrand
		productParser.findPrice = findPrice
		productParser.findProductName = findProductName
		productParser.findImageLink = findImageLink
		productParser.findDescription = findDescription
		productParser.findUrl = findUrl
		return productParser

	def getParser(self):
		def findProductUrls(soup, base_url):
			urls = []
			productCells = soup.find_all("div", class_= "item_pic")
			for cell in productCells: 
				a = cell.find('a')
				if a is not None:
					url = a['href']
					print "Found product url", url
					urls.append(url)
			return urls

		parser = crawler.Parser(self.getProductParser(), findProductUrls)
		return parser 

	def __init__(self): 
		print "Creating Forever21 Crawler"
		self.crawler = crawler.Crawler(['http://www.forever21.com/Product/Category.aspx?br=f21&category=dress&pagesize=100&page=1'], self.getParser())


	def crawl(self):
		self.crawler.crawl()


def findUrls(soup, base_url):
			urls = []
			productCells = soup.findAll("div", class_= "item_pic")
			print productCells
			for cell in productCells: 
				a = cell.find('a')
				if a is not None:
					url = a['href']
					print "Found product url", url
					urls.append(url)
			return urls


#driver = webdriver.Firefox()
url = "http://www.forever21.com/Product/Category.aspx?br=f21&category=dress&pagesize=100&page=1"
#r = driver.get(url)
#html = r.read()
#headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
#html = requests.get(url, headers=headers)
html = urllib.urlopen(url).read()
#response = opener.open(url)
#html = response.read()
soup = BeautifulSoup(html, "html.parser")
print soup
findUrls(soup, url)

#crawler = ForeverCrawler()
#crawler.crawl()
