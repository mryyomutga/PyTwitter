# Pytwitter
twitterの分析プログラム

PythonでTwitter APIへアクセスしていろいろやる

## TODO
- トレンドの取得について機能改善(trendとvolumeだけは寂しい)
- プロフィール変更できるようにする?
- ~~繰り返し実行可能にするために、コマンド対応表を作成する~~(実装したものだけ)
- ~~ツイートに"Pytwitterからの投稿"を組込む~~
- パッケージ化なり外部からimportなりできるようにし、実行専用スクリプトにするとよし
- Twitter機能を実装したメソッドをもう少し加える
- プログラム設計について考える
- リファクタリング
- GUIなど、PytwitterのUIを実装できるとGood!!

## 必要なこと
ライブラリに`Requests_OAuthlib`を用いるため、それのインストール

`$ pip install requests requests_oauthlib`

1. Twitter APIにアクセスするためにアプリケーションの登録をする

	[Twitterの開発者向けサイト](https://apps.twitter.com/app/new)にアクセスして
	- Consumer key
	- Consumer secret
	- Access token
	- Access token secret

	を取得する

	細かいやり方は[ここ](http://website-planner.com/twitter%E3%82%A2%E3%83%97%E3%83%AA%E3%82%B1%E3%83%BC%E3%82%B7%E3%83%A7%E3%83%B3%E3%81%AE%E4%BD%9C%E6%88%90%EF%BC%88consumer-key%E3%80%81consumer-secret%E3%80%81access-token%E3%80%81access-token-secret/)

2. 取得した鍵をjsonファイルに書き込む
	4つの鍵を取得したら`TwitterAPIKey.json`に設定を書き込む

	TwitterAPIKey.jsonは
	```json
	{
		"screen_name":"xxxx"
		"CK":"xxxxxxxxxxxxxxx",
		"CS":"xxxxxxxxxxxxxxx",
		"AT":"xxxxxxxxxxxxxxx",
		"AS":"xxxxxxxxxxxxxxx"
	}

	```

	となっている。

	`screen_name`にtwitterの`@名前`の@抜きのものを書く

	`CK`,`CS`,`AT`,`AS`にはそれぞれのキーを書き込む


## ライブラリ
- Requests-OAuthlib(OAuth認証、リクエスト...)
- json

## 説明
- tweet関数でツイートする
- research関数でキーワードから50件のツイートを取得
- home_timeline関数で自分のタイムラインを取得
- user_timeline関数で指定したユーザーのタイムラインを取得
- place_trend関数で指定した地域のトレンドを取得
- 指定したユーザーのフォロワーを取得
- これらを繰り返し実行
