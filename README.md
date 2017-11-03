# Pytwitter
Twitterの分析プログラム

PythonでTwitter APIへアクセスしていろいろやる

PythonでTwitter APIを扱うライブラリとして`tweepy`や`python-twitter`があるが、これらを使用せず様々な機能を実装したい

出来ればbot機能とかも作りたい

## 説明
開発環境はPython3.6.3なのでそれ以外の環境で動作するかは保証しません(特にPython2系)

| Method                 | Discription |
|:-----------------------|:------------|
| tweet                  | ツイートする |
| get_user_info          | 指定したユーザーの情報を取得する |
| get_follow_request_uid | フォローリクエストの確認とユーザーIDを取得する |
| get_req_user_info      | ユーザーIDからユーザー情報を取得する |
| reply_follow_request   | フォローリクエストしているユーザーに対してリプライを送る |
| create_friend_FolReq   | フォローリクエストしたユーザーをフォローする |
| home_timeline          | 自分のタイムラインを取得する |
| user_timeline          | 指定したユーザーのタイムラインを取得する |
| get_friends            | 指定したユーザーの最新のフォローを50人取得する |
| get_followers          | 指定したユーザーの最新のフォロワーを50人取得する |
| get_all_followers      | 指定したユーザーの全フォロワーを取得する(非推奨) |
| search                 | キーワードから100件のツイートを取得する |
| place_trend            | 指定した地域のトレンドを取得する |
| change_profile         | プロフィールを変更する |

Twitter APIについて詳しい情報は[ここから](https://developer.twitter.com/en.html "Twitter Developer Platform")

- フォローリクエストを出したユーザーに対してリプライを送る(相手には見えない)
- Pytwitter.py内にある`Pytwitter_main`を呼ぶと、Pytwitterシェルが起動し、実装した機能を使用することができる

## 問題点・解決方法
- 鍵垢のユーザーが`get_follow_request_uid`・`get_user_info`・`reply_follow_request`を実行したときにリプライを送っても送信相手から見えない

	- フォローリクエストを出しているユーザーを自動でフォローし、リプライを送る

- 公開しているユーザーが`get_follow_request_uid`・`get_user_info`・`reply_follow_request`を実行したとき、そもそもフォローリクエストは存在しない

	1. 与える引数や前回のPytwitter実行終了時までにフォロワーを取得してログに記録する。

	1. コマンド実行時に現在のフォロワーとログに記録されているフォロワーの差分から自動フォローとリプライを送る相手を決定する

- `get_all_followers`を呼ぶ際、指定したユーザーのフォロワーが多いとTwitterAPIのアクセス制限に引っかかる

	- `https://api.twitter.com/1.1/application/rate_limit_status.json`にリクエストして制限やアクセス回数などを取得し、適切にwaitをかけるなりする

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
		"screen_name":"xxxx",
		"CK":"xxxxxxxxxxxxxxx",
		"CS":"xxxxxxxxxxxxxxx",
		"AT":"xxxxxxxxxxxxxxx",
		"AS":"xxxxxxxxxxxxxxx"
	}

	```

	となっている。

	`screen_name`にtwitterの`@名前`の@抜きのものを書く

	`CK`・`CS`・`AT`・`AS`にはそれぞれのキーを書き込む

## ライブラリ
- print_function

	Python3系でのprint()をPython2系でも使えるようにするライブラリ
- Requests-OAuthlib

	OAuth認証、リクエストなどのライブラリ
- json

	JSON形式のデータを扱うライブラリ
- os

	OSの機能を使用するライブラリ

	主にwindowsやlinuxの`cls`・`clear`を扱う

## コメントなど
- Bot機能を実装するにはnode.jsやdocker、tweepyなどの機能を使わないとできない?

## TODO
- ~~トレンドの取得について機能改善(trendとvolumeだけは寂しい)~~
- ~~色を付けて見やすくする~~
- ~~プロフィール変更できるようにする(要調査)~~
- ~~繰り返し実行可能にするために、コマンド対応表を作成する~~(実装したものだけ)
- ~~ツイートに"Pytwitterからの投稿"を組込む~~
- パッケージ化なり外部からimportなりできるようにし、実行専用スクリプトにするとよし
- ~~Twitter機能を実装したメソッドをもう少し加える~~
- コマンドの実行結果をログに記録する(ファイルの拡張子など要検討)
- ログの記録から様々な機能を提供する(できれば)
- Bot機能の提供
- プログラム設計について考える
- リファクタリング
- GUIなど、PytwitterのUIを実装できるとGood!!
