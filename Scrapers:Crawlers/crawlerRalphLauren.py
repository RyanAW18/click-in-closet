import requests
from bs4 import BeautifulSoup
import json
#import re

params = {"action": "getcategory",
          #"category": re.compile('\S+'),
          "categoryId": "",
          "cp": "",
          "ab": "tn_men_cs_poloshirts",
          "pg": 1}

url = "http://www.ralphlauren.com/Ajax/Ajax_Category.aspx"
test = requests.get(url, params=params)
js = requests.get(url, params=params).json()
soup = BeautifulSoup(js[u'CategoryHTML'], "html.parser")
i = 0
j = 0

while len(soup.select("li.product a")) != 0:
   for a in soup.select("li.product a"):
      #print a["href"]
      i = i + 1

   params["pg"] = params["pg"] + 1
   j = j + 1
   js = requests.get(url, params=params).json()
   soup = BeautifulSoup(js[u'CategoryHTML'], "html.parser")

print i
print j