import os
from flask import Flask,request,abort,render_template
from linebot import (LineBotApi,WebhookHandler)
from linebot.exceptions import (InvalidSignatureError)
from linebot.models import(MessageEvent,TextMessage,TextSendMessage)
import urllib.request
from bs4 import BeautifulSoup
import urllib.parse
import json
import re

YOUR_CHANNEL_SECRET = os.environ["YOUR_CHANNEL_SECRET"]
YOUR_CHANNEL_ACCESS_TOKEN= os.environ["YOUR_CHANNEL_ACCESS_TOKEN"]

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
    # return list[str]
    startstaen = urllib.parse.quote(start_station)
    endstaen = urllib.parse.quote(end_station)
    url0 = 'https://transit.yahoo.co.jp/search/result?from='
    url1 = '&flatlon=&to='
    url2 = '&viacode=&viacode=&viacode=&shin=&ex=&hb=&al=&lb=&sr=&type=1&ws=3&s=&ei=&fl=1&tl=3&expkind=1&ticket=ic&mtf=1&userpass=0&detour_id=&fromgid=&togid=&kw='
    url = url0 + startstaen + url1 + endstaen + url2 + endstaen
    req = urllib.request.urlopen(url)
    html = req.read().decode('utf-8')
    soup = BeautifulSoup(html,'html.parser')
    srline = soup.select("div.elmRouteDetail")
    station=srline[0].select("div#route01 div.routeDetail  div.station")
    fare_section=srline[0].select("div#route01 div.routeDetail div.fareSection")[0]
    fareSection=fare_section.select("div ul li.transport div ")
    send_texts = []
    for i in range(len(srline[0].select("div#route01 div.routeDetail  div.station"))):
      time=station[i].select("ul.time  li")
      time_str = ""
      for j in range(len(time)):
        time_str += time[j].get_text()
      send_texts.append("{}{}".format(station[i].select_one("dl  dt").get_text(),time_str))
    fareSection=fare_section.select("div ul li.transport div ")
    far=fare_section.select("div ul  li.platform")
    # print(far[0].get_text())
    for k in range(len(fareSection)):
      send_texts[k]=send_texts[k]+re.sub("\[train\]","",fareSection[k].get_text())
    for l in range(len(far)):
      send_texts[l]=send_texts[l]+far[l].get_text()
    # print(send_texts)
      # print(fareSection[0].select("ul  li.platform"))
    send_text=""
    for i in range(len(send_texts)):
      send_text+=send_texts[i]+"\n"

    return "{}駅->{}駅区間{}{}\n{}\n{}\n走行距離:{}\n{} ".format(
      start_station,
      end_station,
      srline[0].select_one("div#route01 dl dt").get_text(),
      srline[0].select_one("div#route01  dl  dd:nth-child(2)  ul  li.time").get_text(),
      re.sub("\[priic\]","",srline[0].select_one("div#route01  dl  dd:nth-child(2)  ul  li.fare").get_text()),
      srline[0].select_one("div#route01 dd li.transfer").get_text(),
      srline[0].select_one("div#route01 dd li.distance").get_text(),
      send_text
    )
    # time = soup.select("li.time")
    # arrive=time[2].select_one('span.mark').text.strip()
    # return arrive

@handler.add(MessageEvent,message=TextMessage)
def handler_message(event):
  stations=event.message.text.split(",")
  t_routes=get_train_routes(stations[0],stations[1])
  line_bot_api.reply_message(
    event.reply_token,
    TextMessage(text=t_routes)
    )
if __name__ == "__main__":
  port = int(os.getenv("PORT", 5000))
  app.run(host="0.0.0.0", port=port)
