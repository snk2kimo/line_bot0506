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

line_bot_api = LineBotApi('x8QBVmSD5mA0dQ/G/F22rxW4IUn0Pq81UYBQebcwheylhNYlndaYPwD28eTQ31Rlj0dDCI7ujXyt4TkY9hZmk24HYornhXtyMd64M+QjgCH1QhIb0bboUU56SG2WPD8OoBXpyzBV1s6ME2BCdlup7wdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('e6c93b46b6dad7309eb9891f6a18bc18')


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