# Pytwitter
twitterの分析プログラム

PythonでTwitter APIへアクセスしていろいろやる

## やること
ライブラリに`Requests_OAuthlib`を用いるため、それのインストール

`$ pip install requests requests_oauthlib`

Twitter APIにアクセスするためにアプリケーションの登録をする

[Twitterの開発者向けサイト](https://apps.twitter.com/app/new)にアクセスして
- Consumer key
- Consumer secret
- Access token
- Access token secret

を取得する

細かいやり方は[ここ](http://website-planner.com/twitter%E3%82%A2%E3%83%97%E3%83%AA%E3%82%B1%E3%83%BC%E3%82%B7%E3%83%A7%E3%83%B3%E3%81%AE%E4%BD%9C%E6%88%90%EF%BC%88consumer-key%E3%80%81consumer-secret%E3%80%81access-token%E3%80%81access-token-secret/)

## ライブラリ
- Requests-OAuthlib(OAuth認証、リクエスト...)
- json

## 説明
- tweet関数でツイートする
- research関数でキーワードから50件のツイートを取得
- home_timeline関数で自分のタイムラインを取得
- user_timeline関数で指定したユーザーのタイムラインを取得
- place_trend関数で指定した地域のトレンドを取得
