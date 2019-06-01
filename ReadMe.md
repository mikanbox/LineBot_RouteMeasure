# ルートの長さはかるくん
## 概要
受け取った画像の中の指定の色のドットを数えてその比率を返します










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


heroku config:set CHANNEL_ACCESS_TOKEN="" --app imagelength

heroku config:set CHANNEL_SECRET="" --app imagelength

## 参考
- https://qiita.com/ryoma30/items/d07bd96f8ce3ecefa172


