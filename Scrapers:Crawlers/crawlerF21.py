import requests
from bs4 import BeautifulSoup
import json

params = {"action": "getcategory",
          "br": "f21",
          "category": "dress",
          "pageno": 1,
          "pagesize": "",
          "sort": "",
          "fsize": "",
          "fcolor": "",
          "fprice": "",
          "fattr": ""}

url = "http://www.forever21.com/Ajax/Ajax_Category.aspx"
test = requests.get(url, params=params)
js = requests.get(url, params=params).json()
soup = BeautifulSoup(js[u'CategoryHTML'], "html.parser")
i = 0
j = 0

while len(soup.select("div.item_pic a")) != 0:
   for a in soup.select("div.item_pic a"):
      print a["href"]
      i = i + 1
   params["pageno"] = params["pageno"] + 1
   j = j + 1
   js = requests.get(url, params=params).json()
   soup = BeautifulSoup(js[u'CategoryHTML'], "html.parser")

print i
