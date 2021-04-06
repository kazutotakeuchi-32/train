import urllib.request
from bs4 import BeautifulSoup
import urllib.parse
import re
import requests
from urllib.request import Request, urlopen
import glob
import os
start_station ='川崎'
# end_station = "渋谷"
startstaen = urllib.parse.quote(start_station)
# endstaen = urllib.parse.quote(end_station)

domain ="https://transit.yahoo.co.jp/"
url = domain+"station/search?q={}".format(startstaen)
req = urllib.request.urlopen(url)
html = req.read().decode('utf-8')
ary =[]
soup = BeautifulSoup(html,'html.parser')
station = soup.select("#mdSearchResult  ul:nth-child(3)")
sn = station[0].select("ul li")
for s in range(len(sn)):
  href = sn[s].find("a").get('href')
  url1 = domain+href
  req = urllib.request.urlopen(url1)
  html1 = req.read().decode('utf-8')
  soup1=BeautifulSoup(html1,"html.parser")
  ary.append(re.sub("(\(||\))","",re.search('\([\d.,]*\)',soup1.select("#mdStaAreaMap  div.elmAreaMap img ")[0].get("src")).group()).split(","))
  titles= soup1.select("#mdStaEquip ul.elmStaItem li div h3")
  title=""
  for t in range(len(titles)):
    title+=titles[t].get_text()+" "
  ary[0].append(title)
  contents = soup1.select("#mdStaEquip  ul.elmStaItem li  p")
  content = ""
  for c in range(len(contents)):
    content+= contents[c].get_text()+ "separation"
  ary[0].append(content)
  print(ary)

for i in range(len(ary)):
  print(ary[i][0],ary[i][1])
  # req=Request("https://api.mapbox.com/styles/v1/kazutotakeuchi/ckn4mtjoq0sv117t4g2ul8tn6/static/{},{},15.00,0,0/600x600@2x?access_token=pk.eyJ1Ijoia2F6dXRvdGFrZXVjaGkiLCJhIjoiY2tuNGdtMm9kMWc5aDJ2bHI5OXdxZGdrbiJ9.wcgOy_qruX8ATSmGS3yJsA&logo=false".format(ary[i][0],ary[i][1]))
  print("https://api.mapbox.com/styles/v1/kazutotakeuchi/ckn4mtjoq0sv117t4g2ul8tn6/static/{},{},15.00,0,0/600x600@2x?access_token=pk.eyJ1Ijoia2F6dXRvdGFrZXVjaGkiLCJhIjoiY2tuNGdtMm9kMWc5aDJ2bHI5OXdxZGdrbiJ9.wcgOy_qruX8ATSmGS3yJsA&logo=false".format(ary[i][0],ary[i][1]))
#   with urlopen(req) as res:
#     with open ('./static/map{}.png'.format(i+1), mode='wb') as file:
#       file.write(res.read())
# file_list = glob.glob("./static/map*png")
# for file in file_list:
#     print("remove：{0}".format(file))
#     os.remove(file)
