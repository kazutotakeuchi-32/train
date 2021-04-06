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
  req=Request("https://api.mapbox.com/styles/v1/kazutotakeuchi/ckn4mtjoq0sv117t4g2ul8tn6/static/{},{},15.00,0,0/600x600@2x?access_token=pk.eyJ1Ijoia2F6dXRvdGFrZXVjaGkiLCJhIjoiY2tuNGdtMm9kMWc5aDJ2bHI5OXdxZGdrbiJ9.wcgOy_qruX8ATSmGS3yJsA&logo=false".format(ary[i][0],ary[i][1]))
  with urlopen(req) as res:
    with open ('./static/map{}.png'.format(i+1), mode='wb') as file:
      file.write(res.read())
file_list = glob.glob("./static/map*png")
for file in file_list:
    print("remove：{0}".format(file))
    os.remove(file)






  # ary.append(soup1.select("#mdStaAreaMap  div.elmAreaMap img ")[0].get("src"))

# req = Request("https://api.mapbox.com/styles/v1/mapbox/streets-v11/static/139.69686160004,35.531421503894,15.00,0,0/600x600@2x?access_token=pk.eyJ1Ijoia2F6dXRvdGFrZXVjaGkiLCJhIjoiY2tuNGdtMm9kMWc5aDJ2bHI5OXdxZGdrbiJ9.wcgOy_qruX8ATSmGS3yJsA&logo=false")
# req = Request("https://api.mapbox.com/styles/v1/kazutotakeuchi/ckn4mtjoq0sv117t4g2ul8tn6/static/139.69686160004,35.531421503894,15.00,0,0/600x600@2x?access_token=pk.eyJ1Ijoia2F6dXRvdGFrZXVjaGkiLCJhIjoiY2tuNGdtMm9kMWc5aDJ2bHI5OXdxZGdrbiJ9.wcgOy_qruX8ATSmGS3yJsA&logo=false")
# req = Request("https://api.mapbox.com/styles/v1/kazutotakeuchi/ckn4mtjoq0sv117t4g2ul8tn6/static/139.70091713628,35.532838299108,15.00,0,0/600x600@2x?access_token=pk.eyJ1Ijoia2F6dXRvdGFrZXVjaGkiLCJhIjoiY2tuNGdtMm9kMWc5aDJ2bHI5OXdxZGdrbiJ9.wcgOy_qruX8ATSmGS3yJsA&logo=false")
# req = Request("https://api.mapbox.com/styles/v1/mapbox/streets-v11/static/139.70091713628,35.532838299108,15.00,0,0/600x600@2x?access_token=pk.eyJ1Ijoia2F6dXRvdGFrZXVjaGkiLCJhIjoiY2tuNGdtMm9kMWc5aDJ2bHI5OXdxZGdrbiJ9.wcgOy_qruX8ATSmGS3yJsA&logo=false")
# 'mapbox://styles/mapbox/streets-v11
# print(ary[i])
# # https://api.mapbox.com/styles/v1/yahoojapan/ck353yf380a0k1cmcdx7jc1xq/static/url-https://s.yimg.jp/images/transit/pc/v2/img/map/pinSpot.png(139.70091713628,35.532838299108)/139.70091713628,35.532838299108,16/615x200@2x?access_token=pk.eyJ1IjoieWFob29qYXBhbiIsImEiOiJjazY3Zmw5Z2MwN3Y3M2ttem4xcXhsZnJzIn0.dxIZU7D4wqvqm9o8pUlKjg&logo=false
# print(req)
# # pk.eyJ1Ijoia2F6dXRvdGFrZXVjaGkiLCJhIjoiY2tuNGdqcGgyMXI1dDJvbWZmeWdsb3NjZSJ9.NjlicsAymWrnLKtJSPTRBw
# with urlopen(req) as res:
#   # print(res.read())
#   with open ('map.png', mode='wb') as file:
#     file.write(res.read())
  #     # print(res.read())
  # req =requests.get(ary[i])
  # with urlopen(req) as res:
  # with open ('map.png', mode='wb') as file:
  #   file.write(res.read())

  # print(req.content)
  # with (req as response:
#    the_page = response.read()
  #  print(the_page)
  #  req = urllib.request.Request('http://www.voidspace.org.uk')
  # with open("/Users/kazuto/projects/Python/tralin/sample{}.png".format(i), "wb") as f:
  #   f.write(req.content)


# res = requests.get("https://api.mapbox.com/styles/v1/yahoojapan/ck353yf380a0k1cmcdx7jc1xq/static/url-https://s.yimg.jp/images/transit/pc/v2/img/map/pinSpot.png(139.69686160004,35.531421503894)/139.69686160004,35.531421503894,16/615x200@2x?access_token=pk.eyJ1IjoieWFob29qYXBhbiIsImEiOiJjazY3Zmw5Z2MwN3Y3M2ttem4xcXhsZnJzIn0.dxIZU7D4wqvqm9o8pUlKjg&logo=false", verify=False)
# print(res)
# for t in range(len(ary)):
#  https://api.mapbox.com/styles/v1/mapbox/streets-v11/static/136.8974,35.1774,13.28,0,0/600x600@2x?access_token=YOUR_MAPBOX_ACCESS_TOKEN




# print(ary)
# 14.26/35.5354/139.69967

# https://api.mapbox.com/styles//mapbox/streets-/static/-122.4241,37.78,14.25,0,60/600x600?access_token=pk.eyJ1Ijoia2F6dXRvdGFrZXVjaGkiLCJhIjoiY2tuNGdtMm9kMWc5aDJ2bHI5OXdxZGdrbiJ9.wcgOy_qruX8ATSmGS3yJsA

# https://api.mapbox.com/styles/v1/kazutotakeuchi/ckn4hmxh90nsi17t43l3cb15l.html?fresh=true&title=view&access_token=pk.eyJ1Ijoia2F6dXRvdGFrZXVjaGkiLCJhIjoiY2tuNGdqcGgyMXI1dDJvbWZmeWdsb3NjZSJ9.NjlicsAymWrnLKtJSPTRBw

# https://api.mapbox.com/styles/v1/kazutotakeuchi/ckn4hmxh90nsi17t43l3cb15l/mapbox/streets-v11/static/139.69686160004,35.531421503894,15.00,0,0/600x600@2x?access_token=pk.eyJ1Ijoia2F6dXRvdGFrZXVjaGkiLCJhIjoiY2tuNGdqcGgyMXI1dDJvbWZmeWdsb3NjZSJ9.NjlicsAymWrnLKtJSPTRBw
# https://api.mapbox.com/styles/v1/yahoojapan/ck353yf380a0k1cmcdx7jc1xq/static/url-https://s.yimg.jp/images/transit/pc/v2/img/map/pinSpot.png(139.72616419974,35.535642569681)/139.72616419974,35.535642569681,16/615x200@2x?access_token=pk.eyJ1IjoieWFob29qYXBhbiIsImEiOiJjazY3Zmw5Z2MwN3Y3M2ttem4xcXhsZnJzIn0.dxIZU7D4wqvqm9o8pUlKjg&logo=false
# for i in range(len(ary)):
# https://api.mapbox.com/styles/v1/mapbox://styles/kazutotakeuchi/ckn4hmxh90nsi17t43l3cb15l?access_token=pk.eyJ1Ijoia2F6dXRvdGFrZXVjaGkiLCJhIjoiY2tuNGdqcGgyMXI1dDJvbWZmeWdsb3NjZSJ9.NjlicsAymWrnLKtJSPTRBw
# https://api.mapbox.com/styles/v1/kazutotakeuchi/ckn4hmxh90nsi17t43l3cb15l/tiles/256/2/1394/10@2x?access_token=pk.eyJ1Ijoia2F6dXRvdGFrZXVjaGkiLCJhIjoiY2tuNGdqcGgyMXI1dDJvbWZmeWdsb3NjZSJ9.NjlicsAymWrnLKtJSPTRBw
# https://api.mapbox.com/styles/v1/kazutotakeuchi/ckn4hmxh90nsi17t43l3cb15l.html?fresh=true&title=view&access_token=pk.eyJ1Ijoia2F6dXRvdGFrZXVjaGkiLCJhIjoiY2tuNGdqcGgyMXI1dDJvbWZmeWdsb3NjZSJ9.NjlicsAymWrnLKtJSPTRBw
#https://mapbox://styles/kazutotakeuchi/ckn4hmxh90nsi17t43l3cb15l
# https://api.mapbox.com/styles/v1/kazutotakeuchi/ckn4hmxh90nsi17t43l3cb15l/tiles/256/10/139.69686160004,35.531421503894,15.00,0,0/600x600@@2x?access_token=pk.eyJ1Ijoia2F6dXRvdGFrZXVjaGkiLCJhIjoiY2tuNGdqcGgyMXI1dDJvbWZmeWdsb3NjZSJ9.NjlicsAymWrnLKtJSPTRBw
# /styles/v1/{username}/{style_id}/static/{overlay}/{lon},{lat},{zoom},{bearing},{pitch}|{auto}/{width}x{height}{@2x}
# https://api.mapbox.com/styles/v1/kazutotakeuchi/ckn4hmxh90nsi17t43l3cb15l/139.69686160004,35.531421503894,15.00,0,0/600x600@2x?access_token=pk.eyJ1Ijoia2F6dXRvdGFrZXVjaGkiLCJhIjoiY2tuNGdqcGgyMXI1dDJvbWZmeWdsb3NjZSJ9.NjlicsAymWrnLKtJSPTRBw
# https://api.mapbox.com/styles/v1/kazutotakeuchi/ckn4hmxh90nsi17t43l3cb15l/url-https%3A%2F%2Fs.yimg.jp/139.69686160004,35.531421503894,15.00,0,0/600x600@2x?access_token=pk.eyJ1Ijoia2F6dXRvdGFrZXVjaGkiLCJhIjoiY2tuNGdqcGgyMXI1dDJvbWZmeWdsb3NjZSJ9.NjlicsAymWrnLKtJSPTRBw&logo=false
