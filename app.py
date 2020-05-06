from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)

app = Flask(__name__)

line_bot_api = LineBotApi('K+2k0M/NREd7VPJZfWQ2bwSagCXJjUlwqb3Sy9JDtJCLesHYnOs2iFymTAGFKzUciZOgxvZ3wE/9duc5Zg3PkdEML1hF8LCK9BgAhvp2t3w32VMVSfZWN/cz/pCL4KHFR/lQ7pFmpthUInqvoSKmzQdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('05ae55e375eba367cbd36b5beb2f1fac')


@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        print("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    msg = event.message.text # 將對方訊息存入msg變數
    
    if msg in ['hi', 'HI', 'Hi', '嗨', '你好']:
        s = '嗨，你好!'
    elif '菜單' in msg:
        s = '需要功能提醒的話，可打help'
    elif msg == '你是誰':
        s = '我是誰不重要'

    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=s)
)


if __name__ == "__main__":
    app.run()