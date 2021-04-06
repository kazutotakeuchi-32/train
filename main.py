import os
from flask import Flask,request,abort,render_template,url_for
from linebot import (LineBotApi,WebhookHandler)
from linebot.exceptions import (InvalidSignatureError)
from linebot.models import(
  MessageEvent,
  TextMessage,
  TextSendMessage,
  TemplateSendMessage,
  ButtonsTemplate,
  PostbackAction,
  MessageAction,
  URIAction,
  ImageSendMessage,
  ImageMessage
)
from bs4 import BeautifulSoup
import urllib.parse
import json
import re
from urllib.request import Request, urlopen
import glob
import os


YOUR_CHANNEL_SECRET = os.environ["YOUR_CHANNEL_SECRET"]
YOUR_CHANNEL_ACCESS_TOKEN = os.environ["YOUR_CHANNEL_ACCESS_TOKEN"]
MAPBOX_ACCESS_TOKEN= os.environ["MAPBOX_ACCESS_TOKEN"]

app = Flask(__name__)
line_bot_api = LineBotApi(YOUR_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(YOUR_CHANNEL_SECRET)

@app.route("/index", methods=['GET'])
def index():
    return render_template("index.html")

@app.route("/callback",methods=['POST'])
def callback():
  signature = request.headers['X-Line-Signature']
  body = request.get_data(as_text=True)
  try:
    handler.handle(body,signature)
  except InvalidSignatureError:
    print("Invalid signature. Please check your channel access token/channel secret .")
    abort(400)
  return 'OK'

def get_train_routes(start_station,end_station):
    # 電車の経路情報をスクレイピング
    # 経路　お金　通過駅
    # return str
    startstaen = urllib.parse.quote(start_station)
    endstaen = urllib.parse.quote(end_station)
    url0 = 'https://transit.yahoo.co.jp/search/result?from='
    url1 = '&tlatlon=&togid=&to='
    url2 = '&viacode=&via=&viacode=&via=&viacode=&via=&y=&m=&d=&hh&m=&m1=&type=1&ticket=ic&expkind=1&ws=3&s=0&al=1&shin=1&ex=1&hb=1&lb=1&sr=1&kw='
    url = url0 + startstaen + url1 + endstaen + url2 + endstaen
    req = urllib.request.urlopen(url)
    html = req.read().decode('utf-8')
    soup = BeautifulSoup(html,'html.parser')
    time = soup.select("li.time")
    srline = soup.select("div.elmRouteDetail")
    routes = []
    i=0
    output=""
    while srline[0].select("div#route0{}".format(i+1) )!= [] :
      routes.append(srline[0].select("div#route0{}".format(i+1)))
      i+=1
    for s in range(len(routes)):
      station =routes[s][0].select("div.routeDetail  div.station")
      fare=routes[s][0].select("div.routeDetail div.fareSection")[0]
      fare_section = routes[s][0].select("div.routeDetail div.access div ")
      send_texts = []
      for i in range(len(routes[s][0].select(" div.routeDetail  div.station"))):
        time=station[i].select("ul.time  li")
        time_str = ""
        for j in range(len(time)):
          time_str += time[j].get_text()
        send_texts.append("\n[{}]{}{}".format(i+1,station[i].select_one("dl  dt").get_text().strip(),time_str.strip()))
      far=fare.select("div ul li.platform")
      for k in range(len(fare_section)):
        send_texts[k]=send_texts[k]+re.sub("(\[train\]||\[walk\])","",fare_section[k].get_text())
      for l in range(len(far)):
        send_texts[l]=send_texts[l]+far[l].get_text()
      send_text=""
      for i in range(len(send_texts)):
        send_text+=send_texts[i]
      output+="{}{}\n{}\n{}\n走行距離:{}\n-----------経路情報----------\n{}\n-----------------------------".format(
        routes[s][0].select_one(" dl dt").get_text(),
        routes[s][0].select_one(" dl  dd:nth-child(2)  ul  li.time").get_text(),
        re.sub("\[priic\]","",routes[s][0].select_one("dl  dd:nth-child(2)  ul  li.fare").get_text()),
        routes[s][0].select_one("dd li.transfer").get_text(),
        routes[s][0].select_one("dd li.distance").get_text(),
        send_text.lstrip()
      )
    return "******{}駅-{}駅区間******".format(start_station,end_station)+output

def get_station_equipment(station_name):
  startstaen = urllib.parse.quote(station_name)
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
    content = ""
    for c in range(len(contents)):
      content+= contents[c].get_text()+ "separation"
    if href!=None:
      ary[s].append(content+"\n"+str(href.get_text())+"separation")
    else:
      ary[s].append(content)
  return ary


def buttons_template_message():
   return TemplateSendMessage(
    alt_text='Buttons template',
    template=ButtonsTemplate(
        thumbnail_image_url='https://example.com/image.jpg',
        title='Menu',
        text='Please select',
        actions=[
            PostbackAction(
                label='postback',
                display_text='postback text',
                data='action=buy&itemid=1'
            ),
            MessageAction(
                label='message',
                text='message text'
            ),
            URIAction(
                label='uri',
                uri='http://example.com/'
            )
        ]
    )
  )

def image_message(image_url):
  return  ImageSendMessage(
    original_content_url =  image_url ,
    preview_image_url    =  image_url
  )

@handler.add(MessageEvent,message=TextMessage)
def handler_message(event):
  text=event.message.text
  if len(text.split(","))>=2:
    stations=text.split(",")
    t_routes=get_train_routes(stations[0],stations[1])
    line_bot_api.reply_message(
      event.reply_token,
      TextMessage(text=t_routes)
    )
  elif text=="遅延情報":
    line_bot_api.reply_message(
      event.reply_token,
      TextMessage(text="遅延情報")
    )
  elif text=="駅情報":
    ary=get_station_equipment("川崎")
    for i in range(len(ary)):
      image_url="{}access_token={}&logo=false".format(ary[i][0],MAPBOX_ACCESS_TOKEN)
      line_bot_api.reply_message(
        event.reply_token,
        image_message(image_url)
      )
      station_name=ary[i][1]
      titles = ary[i][2].split(" ")[:-1]
      contents=ary[i][3].split("separation")[:-1]
      output=""
      for j in range(len(titles)):
        output+= "{}{}".format(titles[j],contents[j])
      text="------------------------\n{}\n{}\n-----------------------".format(station_name,output)
      line_bot_api.reply_message(
        event.reply_token,
        TextMessage(text=text)
      )

  else :
    message =  "無効な値が入力されました。"
    line_bot_api.reply_message(
      event.reply_token,
      TextMessage(text=message)
    )

if __name__ == "__main__":
  port = int(os.getenv("PORT", 5000))
  app.run(host="0.0.0.0", port=port)
