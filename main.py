from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage, ImageMessage
)
import os


app = Flask(__name__)

# 環境変数からLINEのトークンを読み込み
YOUR_CHANNEL_ACCESS_TOKEN = os.environ["CHANNEL_ACCESS_TOKEN"]
YOUR_CHANNEL_SECRET = os.environ["CHANNEL_SECRET"]

line_bot_api = LineBotApi(YOUR_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(YOUR_CHANNEL_SECRET)


from PIL import Image
import numpy as np


class ColorDot:
    color = []
    count = 0
    name = ""

    def __init__(self, col, name):
        self.color = np.array(col)
        self.name = name


class DotsColorList:
    ColorList = []

    def addColor(self, col, name):
        item = ColorDot(col, name)
        self.ColorList.append(item)

    def searchDot(self, col):
        for c in self.ColorList:
            if (col == c.color).all():
                c.count += 1

    def outputPrint(self):
        for c in self.ColorList:
            print(c.name + "  " + str(c.count))

    def outputPrintRatio(self):
        default = float(self.ColorList[0].count)
        for c in self.ColorList:
            print(c.name + "  " + '{:.4f}'.format(float(c.count) / default))

    def outputStringRatio(self):
        mes = ""
        default = float(self.ColorList[0].count)
        for c in self.ColorList:
            mes += c.name + "  " + \
                '{:.4f}'.format(float(c.count) / default) + "\n"
        return mes


@app.route("/")
def hello():
    return "Hello World!"


# LINE APIにアプリがあることを知らせるためのもの
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
        abort(400)

    return 'OK'


# メッセージが来た時の反応
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    message_txt = event.message.text

    reply_txt = "ルート画像を送ってね"

    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=reply_txt))


# 画像が来たときの反応
@handler.add(MessageEvent, message=ImageMessage)
def handle_image(event):
    reply_txt = ""
    message_id = event.message.id

    # 画像データを取得する
    message_content = line_bot_api.get_message_content(message_id)
    # image = BytesIO(message_content.content)

    reply_txt = "画像がきた！"

    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=reply_txt))

    # # Pillowで開く
    # img = Image.open(image)

    # # # こっから処理
    # width, height = img.size

    # if (width * height > 700000):
    #     reply_txt = "画像サイズが大きすぎるよ..!!!"
    #     line_bot_api.reply_message(
    #         event.reply_token,
    #         TextSendMessage(text=reply_txt))




    # img_pixels = []
    # for i in range(height * width):
    #     # getpixel((x,y))で左からx番目,上からy番目のピクセルの色を取得し、img_pixelsに追加する
    #     pixcel = img.getpixel((i % width, i / width))
    #     pix = []
    #     pix.append(pixcel[0])
    #     pix.append(pixcel[1])
    #     pix.append(pixcel[2])
    #     pix = np.array(pix)
    #     img_pixels.append(pix)
    # # あとで計算しやすいようにnumpyのarrayに変換しておく
    # img_pixels = np.array(img_pixels)

    # print("  ----------  ")
    # dotsColorList = DotsColorList()
    # dotsColorList.addColor([0, 255, 0], "green")
    # dotsColorList.addColor([0, 0, 255], "Blue")
    # dotsColorList.addColor([255, 255, 0], "Yellow")
    # dotsColorList.addColor([255, 0, 255], "Purpule")
    # dotsColorList.addColor([255, 0, 0], "red")

    # cnt = 0
    # method = dotsColorList.searchDot
    # # 各色の面積をカウント
    # # ボトルネック
    # for i in img_pixels:
    #     method(i)

    # # dotsColorList.outputPrintRatio()

    # reply_txt = dotsColorList.outputStringRatio
    # line_bot_api.reply_message(
    #     event.reply_token,
        # TextSendMessage(text=reply_txt))






if __name__ == "__main__":
    port=int(os.getenv("PORT", 5000))
    app.run(host = "0.0.0.0", port = port)
