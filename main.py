import os
from flask import Flask,request,abort,render_template
from linebot import (LineBotApi,WebhookHandler)
from linebot.exceptions import (InvalidSignatureError)
from linebot.models import(MessageEvent,TextMessage,TextSendMessage)

YOUR_CHANNEL_SECRET = os.environ["YOUR_CHANNEL_SECRET"]
YOUR_CHANNEL_ACCESS_TOKEN= os.environ["YOUR_CHANNEL_ACCESS_TOKEN"]


app = Flask(__name__)
line_bot_api = LineBotApi(YOUR_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(YOUR_CHANNEL_SECRET)

@app.route("/index", methods=['GET'])
def index():
    return render_template("index.html")
    # print("ok")
    # return 'OK'

@app.route("/callback",methods=['POST'])
def callback():
  signature = request.headers['X-Line-Signature']
  print(request.headers)
  print(signature)
  body = request.get_data(as_text=True)
  print(body)
  app.logger.info("Request body: " + body)
  try:
    print(handler.handle(body, signature))
    handler.handle(body, signature)
  except InvalidSignatureError:
    print("Invalid signature. Please check your channel access token/channel secret .")
    abort(400)
  return 'OK'

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
