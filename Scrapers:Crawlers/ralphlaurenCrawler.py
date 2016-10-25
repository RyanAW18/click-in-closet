from bs4 import BeautifulSoup
import urllib
import urllib2
import requests

base_url = "http://www.ralphlauren.com"

def findUrls(base_url):
	productUrls = []
	remUrls = []
	remUrls.append(base_url)
	visitedUrls = dict()
	for i in range(0, len(remUrls)):
		current_url = remUrls[i]
		html = requests.get(current_url)
		soup = BeautifulSoup(html.text, "html.parser")
		visitedUrls[current_url] = True	
		typeTag = soup.find('meta', {"property" : "og:type"})
		if typeTag['content'] is "product":
			productUrls.append(current_url)
		links = soup.findAll("a")
		for link in links:
			print link 
			print link['href']
			# if link['href'] is not None:
			# 	url = link['href']
			# 	if not visitedUrls.has_key(url):
			# 		remUrls.append(url)

	return productUrls

html = requests.get(base_url)
soup = BeautifulSoup(html.text, "html.parser")
#print soup
productUrls = findUrls(base_url)
print productUrls