import os
from flask import Flask,request,abort,render_template
from linebot import (LineBotApi,WebhookHandler)
from linebot.exceptions import (InvalidSignatureError)
from linebot.models import(MessageEvent,TextMessage,TextSendMessage)
import urllib.request
from bs4 import BeautifulSoup
import urllib.parse


YOUR_CHANNEL_SECRET = os.environ["YOUR_CHANNEL_SECRET"]
YOUR_CHANNEL_ACCESS_TOKEN= os.environ["YOUR_CHANNEL_ACCESS_TOKEN"]

app = Flask(__name__)
line_bot_api = LineBotApi(YOUR_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(YOUR_CHANNEL_SECRET)


@app.route("/index", methods=['GET'])
def index():
    return render_template("index.html")
    #print("ok")
    # return 'OK'

@app.route("/callback",methods=['POST'])
def callback():
  signature = request.headers['X-Line-Signature']
  print(request.headers)
  print(signature)
  body = request.get_data(as_text=True)
  stations=body.split(",")
  t_routes=get_train_routes(stations[0],stations[1])
  # reply_train_routes = ""
  # for t in range(len(t_routes)):
  #   reply_train_routes+=""

  app.logger.info("Request body: " + body)
  try:
    # print(handler.handle(body, signature))
    handler.handle(t_routes, signature)
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

    time = soup.select("li.time")
    print(soup.select("li"))
    # print('===到着時間抽出===')
    arrive = time[2].select_one('span.mark').text.strip()
    return arrive




@handler.add(MessageEvent,message=TextMessage)
def handler_message(event):
  line_bot_api.reply_message(
    event.reply_token,
    TextMessage(text=event.message.text)
    )
if __name__ == "__main__":
  # app.run()
  port = int(os.getenv("PORT", 5000))
  app.run(host="0.0.0.0", port=port)
