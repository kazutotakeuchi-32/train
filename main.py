import os
from flask import Flask,request,abort
from linebot import (LineBotApi,WebhookHandler)
from linebot.exceptions import (InvalidSignatureError)
from linebot.models import(MessageEvent,TextMessage,TextSendMessage)

YOUR_CHANNEL_SECRET = os.environ["YOUR_CHNNEL_ACCESS_TOKEN"]
YOUR_CHNNEL_ACCESS_TOKEN = os.environ["YOUR_CHANNEL_SECRET"]

app = Flask(__name__)
line_bot_api = LineBotApi(YOUR_CHANNEL_SECRET)
handler = WebhookHandler(YOUR_CHNNEL_ACCESS_TOKEN)

@app.route("/callback",methods=['POST'])
def callback():
  signature = request.headers['X-Line-Signature']
  body = request.get_data(as_text=True)
  app.logger.info("Request body:"+body)
  try:
    handler.handler(body,signature)
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
  app.run()
