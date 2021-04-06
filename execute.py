import urllib.request
from bs4 import BeautifulSoup
import urllib.parse
import re
import requests
from urllib.request import Request, urlopen
import glob
import os
station_name ='川崎'
startstaen = urllib.parse.quote(station_name)
domain ="https://transit.yahoo.co.jp/"
url = domain+"station/search?q={}".format(startstaen)
req = urllib.request.urlopen(url)
html = req.read().decode('utf-8')
ary =[]
soup = BeautifulSoup(html,'html.parser')
station = soup.select("#mdSearchResult  ul:nth-child(3)")
if station==[]:
  hrefs=re.sub("(\(||\))","",re.search('\([\d.,]*\)',soup.select("#mdStaAreaMap  div.elmAreaMap img ")[0].get("src")).group()).split(",")
  ary.append(["https://api.mapbox.com/styles/v1/kazutotakeuchi/ckn4mtjoq0sv117t4g2ul8tn6/static/{},{},15.00,0,0/600x600@2x?".format(hrefs[0],hrefs[1])])
  ary[0].append(soup.select("#main  div.mainWrp  div.labelLarge  h1")[0].get_text())
  titles= soup.select("#mdStaEquip ul.elmStaItem li div h3")
  title=""
  for t in range(len(titles)):
    title+=titles[t].get_text()+" "
  ary[0].append(title)
  contents = soup.select("#mdStaEquip  ul.elmStaItem li  p")
  href=soup.select_one("#mdStaEquip  ul ul  li  a")
  content = ""
  for c in range(len(contents)):
    content+= contents[c].get_text()+ "separation"
  if href!=None:
    ary[0].append(content+"\n"+str(href.get_text())+"separation")
  else:
    ary[0].append(content)
  station_name=ary[0][1]
  titles = ary[0][2].split(" ")[:-1]
  contents=ary[0][3].split("separation")[:-1]
  output=""
  for j in range(len(titles)):
    output+= "{}{}".format(titles[j],contents[j])
  print("------------------------\n{}\n{}\n-----------------------".format(station_name,output))
else:
  sn = station[0].select("ul li")
  for s in range(len(sn)):
    href = sn[s].find("a").get('href')
    url1 = domain+href
    req = urllib.request.urlopen(url1)
    html1 = req.read().decode('utf-8')
    soup1=BeautifulSoup(html1,"html.parser")
    hrefs=re.sub("(\(||\))","",re.search('\([\d.,]*\)',soup1.select("#mdStaAreaMap  div.elmAreaMap img ")[0].get("src")).group()).split(",")
    ary.append(["https://api.mapbox.com/styles/v1/kazutotakeuchi/ckn4mtjoq0sv117t4g2ul8tn6/static/{},{},15.00,0,0/600x600@2x?".format(hrefs[0],hrefs[1])])
    ary[s].append(soup1.select("#main  div.mainWrp  div.labelLarge  h1")[0].get_text())
    titles= soup1.select("#mdStaEquip ul.elmStaItem li div h3")
    title=""
    for t in range(len(titles)):
      title+=titles[t].get_text()+" "
    ary[s].append(title)
    contents = soup1.select("#mdStaEquip  ul.elmStaItem li  p")
    href=soup1.select_one("#mdStaEquip  ul ul  li  a")
    content=""
    for c in range(len(contents)):
      content+= contents[c].get_text()+ "separation"
    if href!=None:
      ary[s].append(content+"\n"+str(href.get_text())+"separation")
    else:
      ary[s].append(content)
  for i in range(len(ary)):
    station_name=ary[i][1]
    titles = ary[i][2].split(" ")[:-1]
    contents=ary[i][3].split("separation")[:-1]
    output=""
    for j in range(len(titles)):
      output+= "{}{}".format(titles[j],contents[j])
    print("------------------------\n{}\n{}\n-----------------------".format(station_name,output))
