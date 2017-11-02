# -*- coding: utf-8 -*-
# Name      : Pytwitter.py
# Author    : Ryoga Miyamoto
# Outline   : PythonでTwitterAPIにアクセスしていろいろやる
# Twitter APIのラッパーライブラリ(tweepy, python-twitter...)があるが直接APIを呼び出す

# クラス化して、コンストラクタなどで各種設定を行った方がよい?

# Python2でPython3用print()を使用するモジュール
from __future__ import print_function
# Requests,OAuth認証用ライブラリ(たぶんrequestsモジュールが内部にある)
from requests_oauthlib import OAuth1Session
# json形式データを扱うライブラリ
import json
# 画面消去するos.system("cls")
import os

# Tweetを行う
# ハッシュタグや@userなどを自動で検出する
def tweet():
    # メッセージリスト
    mes_list = list()
    # mes_list.append("Pytwitterからの投稿")
    # ツイートフォーム
    print("つぶやく内容を入力してください(\"<END>\"で入力終了)")
    mes_list.append(input(termname))
    while mes_list[-1] != "<END>":
        mes_list.append(input(termname))

    print("------------------------------------------------")
    # <<ENDを取り除く
    mes_list.pop()
    mes = "\n".join(mes_list)

    # リクエストに付与するパラメータ
    params = {"status":mes}

    # OAuth認証をし、POSTメソッドでツイート
    session = OAuth1Session(myinfo["CK"], myinfo["CS"], myinfo["AT"], myinfo["AS"])
    req = session.post(URL["tweet"], params=params)

    if req.status_code == 200:
        print("<< Succeed!\n")
        # log.append(mes)
    else:
        print("<< ERROR! : {0}".format(req.status_code))

# 自分のタイムラインを取得する
def home_timeline():
    print("自分のタイムラインを取得します")
    print(termname)
    print("------------------------------------------------")

    # リクエストに付与するパラメータ
    params = {"count":50}

    # OAuth認証をし、GETメソッドで自分のタイムラインを取得
    session = OAuth1Session(myinfo["CK"], myinfo["CS"], myinfo["AT"], myinfo["AS"])
    res = session.get(URL["home_timeline"], params=params)

    # レスポンスをJSON形式に変換
    tweets = json.loads(res.text)

    if res.status_code == 200:
        print("<< Succeed!")
        for tweet in tweets:
            print("+----------------------------------------------+")
            mes = " @{0}: {1}\n created at {2}\n {3}".format(
                tweet["user"]["screen_name"],
                tweet["user"]["name"],
                tweet["created_at"],
                tweet["text"]
                )
            print(mes)
            # log.append(message)
        print("+----------------------------------------------+")
    else:
        print("<< ERROR! : {0}".format(res.status_code))

# 指定したscreen_nameのタイムラインを取得
def user_timeline():
        print("指定したユーザーのタイムラインを取得します")
        print("@screen_nameを入力してください")
        user = input(termname)
        print("------------------------------------------------")

        # リクエストに付与するパラメータ
        params = {"screen_name":user,
                  "count":50}

        # OAuth認証をし、GETメソッドでユーザーのタイムラインを取得
        session = OAuth1Session(myinfo["CK"], myinfo["CS"], myinfo["AT"], myinfo["AS"])
        res = session.get(URL["user_timeline"], params=params)

        # レスポンスをJSON形式に変換
        tweets = json.loads(res.text)

        if res.status_code == 200:
            print("<< Succeed!")
            for tweet in tweets:
                print("+----------------------------------------------+")
                mes = " @{0}: {1}\n created at {2}\n {3}".format(
                    tweet["user"]["screen_name"],
                    tweet["user"]["name"],
                    tweet["created_at"],
                    tweet["text"]
                    )
                print(mes)
                # log.append(message)
            print("+----------------------------------------------+")
        else:
            print("<< ERROR! : {0}".format(res.status_code))

# 指定したユーザーのフォロワーを取得する
def followers_list():
    print("ユーザーを指定してください")
    user = input(termname)
    print("------------------------------------------------")

    # リクエストに付与するパラメータ
    params = {
        "screen_name":user,
        "count":200
    }

    # OAuth認証をし、GETメソッドでフォロワーを取得
    session = OAuth1Session(myinfo["CK"], myinfo["CS"], myinfo["AT"], myinfo["AS"])
    res = session.get(URL["followers_list"], params = params)

    # レスポンスをJSON形式に変換
    tweets = json.loads(res.text)

    if res.status_code == 200:
        print("<< Succeed!")
        for tweet in tweets["users"]:
            print("+----------------------------------------------+")
            mes = " @{0}: {1}\n Created at {2}\n Followers: {3}\n Friends: {4}\n Location: {5}\n URL: {6}\n {7} tweet".format(
                tweet["screen_name"],
                tweet["name"],
                tweet["created_at"],
                tweet["followers_count"],
                tweet["friends_count"],
                tweet["location"],
                tweet["url"],
                tweet["statuses_count"]
                )
            print(mes)
            # log.append(mes)
        print("+----------------------------------------------+")
    else:
        print("<< ERROR! : {0}".format(req.status_code))

# ツイート内容に対してキーワード検索を行う
def search():
    global log
    print("検索する内容を入力してください")
    keyword = input(termname)

    # リクエストに付与するパラメータ
    params = {"q":keyword,
              "locale":"ja",
              "result_type":"recent",
              "count":50}

    # OAuth認証をし、GETメソッドでキーワード検索
    session = OAuth1Session(myinfo["CK"], myinfo["CS"], myinfo["AT"], myinfo["AS"])
    res = session.get(URL["search"], params = params)

    # レスポンスをJSON形式に変換
    tweets = json.loads(res.text)

    if res.status_code == 200:
        print("<< Succeed!")
        for tweet in tweets["statuses"]:
            print("+----------------------------------------------+")
            mes = " @{0}: {1}\n Created at {2}\n {3}".format(
                tweet["user"]["screen_name"],
                tweet["user"]["name"],
                tweet["created_at"],
                tweet["text"]
                )
            print(mes)
            # log.append(mes)
        print("+----------------------------------------------+")
    else:
        print("<< ERROR! : {0}".format(req.status_code))

# 地域のトレンドを取得
def place_trend():
    print("地域を指定してください")
    place = input(termname)
    print("------------------------------------------------")

    # リクエストに付与するパラメータ
    params = {"id":place_code[place]["woeid"]}

    # OAuth認証をし、GETメソッドで地域のトレンドを取得
    session = OAuth1Session(myinfo["CK"], myinfo["CS"], myinfo["AT"], myinfo["AS"])
    res = session.get(URL["place_trend"], params=params)

    # レスポンスをJSON形式に変換
    tweets = json.loads(res.text)

    if res.status_code == 200:
        print("<< Succeed!")
        # 他のJSONと少し違うせいか[0]["trends"]じゃないと取得できない
        for tweet in tweets[0]["trends"]:
            print("+----------------------------------------------+")
            mes = " trends: {0}\n volume: {1}".format(
                tweet["name"],
                tweet["tweet_volume"]
                )
            print(mes)
            # log.append(message)
        print("+----------------------------------------------+")
    else:
        print("<< ERROR! : {0}".format(res.status_code))

# cmd_mesを表示する関数
def print_cmd_mes():
    print("+------------------+")
    for s in cmd_mes:
        print(s)
    print("+------------------+")

# 繰り返し実行する関数
def Pytwitter_main():
    # プログラム終了フラグ
    Escape = False

    for (index, value) in enumerate(cmd_list):
        cmd_mes.append(" {0:<2}: {1}".format(index + 1, value))

    print("コマンドリスト")
    print_cmd_mes()

    # Pytwitterの起動
    while Escape == False:
        print("何をしますか?")
        cmd = input(termname)
        # 入力されたコマンドがリストに存在するか
        if cmd in cmd_list:
            # コンソール画面の消去
            # OSの判定
            if os.name == "nt":
                os.system("CLS")
            else:
                os.system("clear")

            # コマンドの実行
            if cmd == cmd_list[0]:
                tweet()
            elif cmd == cmd_list[1]:
                home_timeline()
            elif cmd == cmd_list[2]:
                user_timeline()
            elif cmd == cmd_list[3]:
                followers_list()
            elif cmd == cmd_list[4]:
                search()
            elif cmd == cmd_list[5]:
                place_trend()
            elif cmd == cmd_list[6]:
                print_cmd_mes()
            elif cmd == cmd_list[7]:
                Escape = True
        else:
            print("{0}はコマンドじゃないよ".format(cmd))

    print("Good Bye!!")


def home_timeline_bot():
    print("自分のタイムラインを取得します")
    print(termname)
    print("------------------------------------------------")

    # リクエストに付与するパラメータ
    params = {"count":50}

    # OAuth認証をし、GETメソッドで自分のタイムラインを取得
    session = OAuth1Session(myinfo["CK"], myinfo["CS"], myinfo["AT"], myinfo["AS"])
    res = session.get(URL["home_timeline"], params=params)

    # レスポンスをJSON形式に変換
    tweets = json.loads(res.text)

    if res.status_code == 200:
        print("<< Succeed!")
        for tweet in tweets:
            print("+----------------------------------------------+")
            mes.append(" @{0}: {1}\n created at {2}\n {3}".format(
                tweet["user"]["screen_name"],
                tweet["user"]["name"],
                tweet["created_at"],
                tweet["text"]
                ))
            return "\n".join(mes)
            # log.append(message)
        print("+----------------------------------------------+")
    else:
        print("<< ERROR! : {0}".format(res.status_code))



# importされた場合は呼ばれない
if __name__ == '__main__':

    # リクエスト送信用URL
    # Twitterの開発者用のページを参照
    # URL:https://developer.twitter.com/en/docs
    URL = {
        "tweet":"https://api.twitter.com/1.1/statuses/update.json",
        "home_timeline":"https://api.twitter.com/1.1/statuses/home_timeline.json",
        "user_timeline":"https://api.twitter.com/1.1/statuses/user_timeline.json",
        "followers_list":"https://api.twitter.com/1.1/followers/list.json",
        "search":"https://api.twitter.com/1.1/search/tweets.json",
        "place_trend":"https://api.twitter.com/1.1/trends/place.json"
    }

    # 取得したツイートのログリスト
    log = list()

    # TwitterAPIKey.jsonからKeyの読み出し
    with open("TwitterAPIKey.json", "r", encoding="utf-8") as f:
        myinfo = json.load(f)

    # 地域情取得用WOEIDの読み出し
    # URL:https://shun1adhocblog.wordpress.com/2013/01/01/twitterapi%E3%82%92%E4%BD%BF%E3%81%A3%E3%81%A6%E3%81%BF%E3%82%8B%E3%83%86%E3%82%B9%E3%83%88by-python/
    with open("woeid.json", "r", encoding="utf-8") as f:
        place_code = json.load(f)

    # アカウント名を表示する場合
    name = "@" + myinfo["screen_name"]
    termname = name + " >> "
    # termname = ">> "

    # コマンドリスト
    cmd_mes = list()
    cmd_list =("tweet",
               "home_timeline",
               "user_timeline",
               "followers_list",
               "search",
               "place_trend",
               "check",         # コマンドリストの確認
               "escape"         # プログラムの終了
               )

    # tweet()
    home_timeline_bot()
    # user_timeline()
    # followers_list()
    # search()
    # place_trend()

    # twitter_main()
    # print_cmd_mes()

    # ログに書き出す
    # with open("PytwitterLog.log", "a+", encoding="utf-8") as f:
    #     for l in log:
    #         f.write(l)
