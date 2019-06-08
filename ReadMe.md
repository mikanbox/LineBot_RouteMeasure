# ルートの長さはかるくん
## 概要
受け取った画像の中の指定の色のドットを数えてその比率を返します


## setup
heroku config:set CHANNEL_ACCESS_TOKEN="" --app imagelength
heroku config:set CHANNEL_SECRET="" --app imagelength
git remote add heroku heroku_git_url

## 手元で動かす
export CHANNEL_ACCESS_TOKEN
export CHANNEL_SECRET
python hello.py
FlaskのcallbackはPOSTメソッドなので、ブラウザからは確認できないよ!!

## mainのコード概要









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



## loginできないときは下記を参考
http://neos21.hatenablog.com/entry/2019/02/14/080000

## 参考資料
- https://qiita.com/ryoma30/items/d07bd96f8ce3ecefa172


