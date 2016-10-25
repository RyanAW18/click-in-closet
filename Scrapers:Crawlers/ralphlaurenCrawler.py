from bs4 import BeautifulSoup
import urllib
import urllib2
import requests

def findUrls(soup, base_url):
			urls = []
			productCells = soup.findAll("a", class_= "photo")
			for cell in productCells: 
				if cell is not None:
					url = cell['href']
					print "Found product url", url
					#urls.append(url)
			#return urls



url = "http://www.ralphlauren.com/family/index.jsp?categoryId=4332103&cp=1760782&ab=tn_women_cs_dresses"
html = requests.get(url)
soup = BeautifulSoup(html.text, "html.parser")
#print soup
findUrls(soup, url)