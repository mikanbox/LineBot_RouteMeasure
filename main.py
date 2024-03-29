from flask import Flask, request, abort
from linebot import (LineBotApi, WebhookHandler)
from linebot.exceptions import (InvalidSignatureError)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
    SourceUser, SourceGroup, SourceRoom,
    TemplateSendMessage, ConfirmTemplate, MessageAction,
    ButtonsTemplate, ImageCarouselTemplate, ImageCarouselColumn, URIAction,
    PostbackAction, DatetimePickerAction,
    CameraAction, CameraRollAction, LocationAction,
    CarouselTemplate, CarouselColumn, PostbackEvent,
    StickerMessage, StickerSendMessage, LocationMessage, LocationSendMessage,
    ImageMessage, VideoMessage, AudioMessage, FileMessage,
    UnfollowEvent, FollowEvent, JoinEvent, LeaveEvent, BeaconEvent,
    FlexSendMessage, BubbleContainer, ImageComponent, BoxComponent,
    TextComponent, SpacerComponent, IconComponent, ButtonComponent,
    SeparatorComponent, QuickReply, QuickReplyButton
)
import os
from io import BytesIO
from tinydb import TinyDB, Query
from PIL import Image
import numpy as np
import base64

app = Flask(__name__)

# 環境変数からLINEのトークンを読み込み
YOUR_CHANNEL_ACCESS_TOKEN = os.environ["CHANNEL_ACCESS_TOKEN"]
YOUR_CHANNEL_SECRET = os.environ["CHANNEL_SECRET"]

line_bot_api = LineBotApi(YOUR_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(YOUR_CHANNEL_SECRET)



#データベースの作成
db = TinyDB('userData.json')
_diff = 20



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

    def removeColor(self):
        self.ColorList.clear()

    def searchDot(self, col):
        for c in self.ColorList:
            if (col == c.color).all():
                c.count += 1

    def searchDotNear(self, col):
        for c in self.ColorList:
            ival = True
            for (coli, ci) in zip(col, c.color):
                if (not (int(ci) <= int(coli) + _diff and int(ci) >= int(coli) - _diff)):
                    ival = False
            if (ival):
                c.count += 1

    def outputPrint(self):
        for c in self.ColorList:
            print(c.name + "  " + str(c.count))

    def outputPrintRatio(self):
        default = float(self.ColorList[0].count)+0.000001
        for c in self.ColorList:
            print(c.name + "  " + '{:.4f}'.format(float(c.count) / default))

    def outputStringRatio(self):
        mes = ""
        default = float(self.ColorList[0].count)
        for c in self.ColorList:
            mes += c.name + "  " + \
                '{:.4f}'.format(float(c.count) / default) + "\n"
        return mes

def push_textMessage(user_id,texts):
    line_bot_api.push_message(to=user_id,
                          messages=TextSendMessage(text=texts)
                          )


bubble = BubbleContainer(
    direction='ltr',
    body=BoxComponent(
        layout='vertical',
        contents=[
            TextComponent(text='ルートで使う色を登録してね', weight='bold', size='xl')
        ]
    ),
    footer=BoxComponent(
        layout='vertical',
        spacing='sm',
        contents=[
            SpacerComponent(size='sm'),
            ButtonComponent(
                style='primary', height='sm',
                action=PostbackAction(label='赤 ff0000', data='c_red'),
                color='#ff4444'
            ),
            SeparatorComponent(),
            ButtonComponent(
                style='primary', height='sm',
                action=PostbackAction(label='青 0000ff', data='c_blue'),
                color='#4444ff'
            ),
            SeparatorComponent(),
            ButtonComponent(
                style='secondary', height='sm',
                action=PostbackAction(label='黄 ffff00', data='c_yellow'),
                color='#ffff44'
            ),
            SeparatorComponent(),
            ButtonComponent(
                style='secondary', height='sm',
                action=PostbackAction(label='マゼンタ ff00ff', data='c_mazenta'),
                color='#ff44ff'
            ),
            SeparatorComponent(),
            ButtonComponent(
                style='secondary', height='sm',
                action=PostbackAction(label='シアン 00ffff', data='c_cian'),
                color='#44ffff'
            ),
            SeparatorComponent(),
            ButtonComponent(
                style='primary',margin='xxl',
                action=PostbackAction(label='比較実行', data='run')
            )
        ]
    )
)





#  flex message送るだけ
def flexMessage(event):
    print("sendFlex")
    reply_txt = ""

    Flexmessage = FlexSendMessage(alt_text="hello", contents=bubble)
    line_bot_api.reply_message(
        event.reply_token,
        Flexmessage
    )


@app.route("/")
def hello():
    return "Hello World!"



# LINE APIにアプリがあることを知らせるためのもの
@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return 'OK'


# メッセージが来た時の反応
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    message_txt = event.message.text
    user_id = event.source.user_id
    print("user_id : " + user_id)

    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text="ルート画像を送ってね"))


# ポストバックイベントでカラーを登録する
@handler.add(PostbackEvent)
def handle_postback(event):
    reply_token = event.reply_token
    user_id = event.source.user_id
    postback_msg = event.postback.data
    print("user_id : " + user_id)



    que = Query()
    if not (db.search(que.id == user_id) ):
        push_textMessage(user_id, "先に画像を上げてね！")
        return



    reply_txt = "エラー　色が存在しません。"
    if postback_msg == 'run':
        userdat = db.search(que.id == user_id)
        colors = userdat[0]['color']
        img = userdat[0]['imgbin']
        if len(colors) > 0:
            reply_txt = RunCompareLines(user_id,img,colors)
            db.remove(que.id  == user_id)

        else:
            reply_txt = "エラー　ルートの色が登録されてないよ"
    else:

        userdat = db.search(que.id == user_id)
        colors = userdat[0]['color']

        if postback_msg == 'c_red':
            colors.append([[255, 0, 0], "red"])
            reply_txt = "赤色を登録したよ"
        elif postback_msg == 'c_blue':
            reply_txt = "青色を登録したよ"
            colors.append([[0, 0, 255], "blue"])
        elif postback_msg == 'c_yellow':
            reply_txt = "黄色を登録したよ"
            colors.append([[255, 255, 0], "Yellow"])
        elif postback_msg == 'c_cian':
            reply_txt = "シアンを登録したよ"
            colors.append([[0, 255, 255], "Cian"])
        elif postback_msg == 'c_mazenta':
            reply_txt = "マゼンタを登録したよ"
            colors.append([[255, 0, 255], "Mazenta"])

        db.update({'color':colors}, que.id == user_id)


    push_textMessage(user_id, reply_txt)

# 画像が来たときの反応
@handler.add(MessageEvent, message=ImageMessage)
def handle_image(event):
    message_id = event.message.id
    user_id = event.source.user_id
    img = line_bot_api.get_message_content(message_id)
    print("user_id : " + user_id)


    que = Query()
    if db.search(que.id == user_id):
        db.remove(que.id  == user_id)

    db.insert({
              'id':user_id,
              'color':[],
              'imgbin':base64.b64encode(img.content).decode('utf-8')
     })

    # flex messageを送信
    flexMessage(event)




def RunCompareLines(userid,img,colors):
    # # Pillowで開く
    img_binary = base64.b64decode(img)
    img_binary = BytesIO(img_binary)

    img = Image.open(img_binary)

    # # こっから処理
    width, height = img.size

    if (width * height > 700000):
        reply_txt = "画像サイズが大きすぎるよ..!!!"
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=reply_txt))

    img_pixels = []
    for i in range(height * width):
        # getpixel((x,y))で左からx番目,上からy番目のピクセルの色を取得し、img_pixelsに追加する
        pixcel = img.getpixel((i % width, i / width))
        pix = []
        pix.append(pixcel[0])
        pix.append(pixcel[1])
        pix.append(pixcel[2])
        pix = np.array(pix)
        img_pixels.append(pix)
    # あとで計算しやすいようにnumpyのarrayに変換しておく
    img_pixels = np.array(img_pixels)

    print("  ----------  ")
    dotsColorList = DotsColorList()
    for c in colors:
        dotsColorList.addColor(c[0], c[1])

    cnt = 0
    method = dotsColorList.searchDotNear
    # 各色の面積をカウント
    # ボトルネック
    for i in img_pixels:
        method(i)

    reply_txt = dotsColorList.outputStringRatio()
    dotsColorList.removeColor()

    return reply_txt




if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    app.run(host="0.0.0.0", port=port)


