# -*- coding: utf-8 -*-
# Pytwitter.py
# Author    : Ryoga Miyamoto

# Python2でPython3用print()を使用するモジュール
from __future__ import print_function
# Requests,OAuth認証用ライブラリ
from requests_oauthlib import OAuth1Session
# json形式データを扱うライブラリ
import json

# TODO: トレンドの取得について機能改善(trendとvolumeだけは寂しい)
# TODO: プロフィール変更できるようにする
# TODO: 繰り返し実行可能にするために、コマンド対応表を作成する
# TODO: パッケージ化なり外部からimportなりできるようにし、実行専用スクリプトにするとよし
# TODO: Twitter機能を実装したメソッドを加える
# TODO: プログラム設計について考える
# TODO: リファクタリング
# TODO: GUIなど、PytwitterのUIを実装できるとGood!!
# リクエスト送信用URL
# URL:https://developer.twitter.com/en/docs
URL = {
    "tweet":"https://api.twitter.com/1.1/statuses/update.json",
    "home_timeline":"https://api.twitter.com/1.1/statuses/home_timeline.json",
    "user_timeline":"https://api.twitter.com/1.1/statuses/user_timeline.json",
    "search":"https://api.twitter.com/1.1/search/tweets.json",
    "place_trend":"https://api.twitter.com/1.1/trends/place.json"
}

# 取得したツイートのログリスト
log = list()

# TwitterAPIKey.jsonからKeyの読み出し
with open("MyTwitterAPIKey.json", "r", encoding="utf-8") as f:
    myinfo = json.load(f)

# 地域情取得用WOEIDの読み出し
# URL:https://shun1adhocblog.wordpress.com/2013/01/01/twitterapi%E3%82%92%E4%BD%BF%E3%81%A3%E3%81%A6%E3%81%BF%E3%82%8B%E3%83%86%E3%82%B9%E3%83%88by-python/
with open("woeid.json", "r", encoding="utf-8") as f:
    place_code = json.load(f)

name = myinfo["screen_name"]
termname = name + " >> "

# Tweetを行う
def tweet():
    # メッセージリスト
    mes_list = list()
    # ツイートフォーム
    print("つぶやく内容を入力してください(\"<<END\"で入力終了)")
    mes_list.append(input(termname))
    while mes_list[-1] != "<<END":
        mes_list.append(input(termname))

    print("------------------------------------------------")
    # <<ENDを取り除く
    mes_list.pop()
    mes = "\n".join(mes_list)

    # リクエストに付与するパラメータ
    params = {"status":mes}

    # OAuth認証をし、POSTリクエストでツイート
    session = OAuth1Session(myinfo["CK"], myinfo["CS"], myinfo["AT"], myinfo["AS"])
    req = session.post(URL["tweet"], params=params)

    if req.status_code == 200:
        print(name + " << Succeed!\n")
        # log.append(mes)
    else:
        print(name + " << ERROR! : {0}".format(req.status_code))

# 自分のタイムラインを取得する
def home_timeline():
    print("自分のタイムラインを取得します")
    print(termname)
    print("------------------------------------------------")

    # リクエストに付与するパラメータ
    params = {"count":50}
    session = OAuth1Session(myinfo["CK"], myinfo["CS"], myinfo["AT"], myinfo["AS"])
    res = session.get(URL["home_timeline"], params=params)

    # レスポンスをJSON形式に変換
    tweets = json.loads(res.text)

    if res.status_code == 200:
        print(name + " << Succeed!")
        print("------------------------------------------------")
        for tweet in tweets:
            mes = "@{0}: {1}\nDate: {2}\n{3}\n".format(
                tweet["user"]["screen_name"],
                tweet["user"]["name"],
                tweet["created_at"],
                tweet["text"]
                )
            print(mes)
            # log.append(message)
        print("------------------------------------------------")
    else:
        print(name + " << ERROR! : {0}".format(res.status_code))

# 指定したscreen_nameのタイムラインを取得
def user_timeline():
        print("指定したスクリーンネームのタイムラインを取得します")
        print("@screen_nameを入力してください")
        screen_name = input(termname)
        print("------------------------------------------------")

        # リクエストに付与するパラメータ
        params = {"screen_name":screen_name,
                  "count":50}

        session = OAuth1Session(myinfo["CK"], myinfo["CS"], myinfo["AT"], myinfo["AS"])
        res = session.get(URL["user_timeline"], params=params)

        # レスポンスをJSON形式に変換
        tweets = json.loads(res.text)

        if res.status_code == 200:
            print(name + " << Succeed!")
            print("------------------------------------------------")
            for tweet in tweets:
                mes = "@{0}: {1}\nDate: {2}\n{3}\n".format(
                    tweet["user"]["screen_name"],
                    tweet["user"]["name"],
                    tweet["created_at"],
                    tweet["text"]
                    )
                print(mes)
                # log.append(message)
            print("------------------------------------------------")
        else:
            print(name + " << ERROR! : {0}".format(res.status_code))

# ツイート内容に対してキーワード検索を行う
def research():
    global log
    print("検索する内容を入力してください")
    keyword = input(termname)

    # リクエストに付与するパラメータ
    params = {"q":keyword,
              "locale":"ja",
              "result_type":"recent",
              "count":50}

    # OAuth認証をし、GETリクエストで検索
    session = OAuth1Session(myinfo["CK"], myinfo["CS"], myinfo["AT"], myinfo["AS"])
    res = session.get(URL["search"], params = params)

    # レスポンスをJSON形式に変換
    tweets = json.loads(res.text)

    if res.status_code == 200:
        print(name + " << Succeed!")
        print("------------------------------------------------")
        for tweet in tweets["statuses"]:
            mes = "@{0}: {1}\nDate: {2}\n{3}\n".format(
                tweet["user"]["screen_name"],
                tweet["user"]["name"],
                tweet["created_at"],
                tweet["text"]
                )
            print(mes)
            # log.append(mes)
        print("------------------------------------------------")
    else:
        print(name + " << ERROR! : {0}".format(req.status_code))

# 地域のトレンドを取得
def place_trend():
    print("地域を指定してください")
    place = input(termname)
    print("------------------------------------------------")

    # リクエストに付与するパラメータ
    params = {"id":place_code[place]["woeid"]}

    session = OAuth1Session(myinfo["CK"], myinfo["CS"], myinfo["AT"], myinfo["AS"])
    res = session.get(URL["place_trend"], params=params)

    # レスポンスをJSON形式に変換
    tweets = json.loads(res.text)

    if res.status_code == 200:
        print(name + " << Succeed!")
        print("------------------------------------------------")
        # 他のJSONと少し違うせいか[0]["trends"]じゃないと取得できない
        for tweet in tweets[0]["trends"]:
            mes = "trends: {}\nvolume: {}\n".format(
                tweet["name"],
                tweet["tweet_volume"]
                )
            print(mes)
            # log.append(message)
        print("------------------------------------------------")
    else:
        print(name + " << ERROR! : {0}".format(res.status_code))

# Pytwitter実行
# tweet()
# home_timeline()
# user_timeline()
# research()
place_trend()

# ログに書き出す
# with open("PytwitterLog.log", "a+", encoding="utf-8") as f:
#     for l in log:
#         f.write(l)
