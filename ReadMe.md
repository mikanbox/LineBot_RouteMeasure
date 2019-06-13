# ルートの長さはかるくん
## 概要
受け取った画像の中の指定の色のドットを数えてその比率を返します


## setup
heroku config:set CHANNEL_ACCESS_TOKEN="" --app imagelength
heroku config:set CHANNEL_SECRET="" --app imagelength
git remote add heroku heroku_git_url

## 手元で動かす
export CHANNEL_ACCESS_TOKEN=xxxxxxxxxxxxxx
export CHANNEL_SECRET=xxxxxxxxxxxxxx
python main.py
FlaskのcallbackはPOSTメソッドonlyなので、ブラウザからは確認できないよ!!

## mainのコード概要




## タスク
<!-- - 複数同時アクセスに対応(辞書作って、ユーザーidとステート作る) -->
<!-- - カラーは事前に問い合わせする形にする -->
  <!-- - 基本的にbot側が持ってて、画像にある色に反応してあるやつだけ表示する -->
  <!-- - Flexメッセージに色一覧を表示して、そこから使う色を選んでもらう -->
  <!-- - 最初に画像送る -->
- 使い方を説明する




## フォルダ構成
- main.py
  - サービスのコード. Flask
- Procfile
  - デプロイ時に実行するコマンド
- requirements.txt
  - デプロイ時にインストールするパッケージ
  - pip show package で確認
- runtime.txt
  - デプロイ先で使用する言語とバージョン

## webhook URL
- https://linebot-ryotei-kun.herokuapp.com/callback


## debug
- https://qiita.com/yamatmoo/items/8d5c2ffe6edf54c91957

python main.py
ngrok http 5000
LINEのwebhook URLに登録


- heroku log 見る
  - heroku logs -a imagelength --tail

## loginできないときは下記を参考
http://neos21.hatenablog.com/entry/2019/02/14/080000

## 参考資料
- https://qiita.com/ryoma30/items/d07bd96f8ce3ecefa172
- FlexMessage Sim
  - https://developers.line.biz/console/fx/
- https://developers.line.biz/ja/reference/messaging-api/#postback-action

