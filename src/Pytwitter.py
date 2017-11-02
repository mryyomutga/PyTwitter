# -*- coding: utf-8 -*-
# Name      : Pytwitter.py
# Author    : Ryoga Miyamoto
# Outline   : PythonでTwitterAPIにアクセスしていろいろやる
# Env       : Python3.6.3
# Twitter APIのラッパーライブラリ(tweepy, python-twitter...)があるが直接APIを呼び出す

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
# Argument : None
# Return  : None
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
    # <END>を取り除く
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
    # リクエスト失敗
    else:
        print("<< ERROR! : {0}".format(req.status_code))

# フォローリクエストを確認する
# Argument : None
# Return  :
# Succeed : Response["ids"](User_ID_list)
# Error   : HTTP status code is not 200(-1) or Not follow requests(-2)
def get_follow_requests():
    print("フォローリクエストを確認します")
    print("------------------------------------------------")
    params = {"cursor":-1,
              "stringify_ids":True}

    # OAuth認証をし、GETメソッドでフォローリクエストの取得
    session = OAuth1Session(myinfo["CK"], myinfo["CS"], myinfo["AT"], myinfo["AS"])
    res = session.get(URL["friendships_incoming"], params=params)

    # レスポンスをJSON形式に変換
    str_id = json.loads(res.text)

    if res.status_code == 200:
        print("<< Succeed!")
    # リクエスト失敗
    else:
        print("<< ERROR! : {0}".format(res.status_code))
        return -1

    # フォローリクエストがない
    if len(str_id["ids"]) == 0:
        print("フォローリクエストはありませんでした...")
        return -2

    # フォローリクエストを出したIDの一覧
    print("+----------------------------------------------+")
    print(" Get follow-request user's id")
    for (index, usr_id) in enumerate(str_id["ids"]):
        print(" {0:<3} : {1}".format(index + 1, usr_id))
    print("+----------------------------------------------+")

    return str_id["ids"]

# ユーザーIDからユーザー情報を取得する
# Argument : User ID list
# Return  :
# Succeed : get user's Screen Name list(scr_name_list)
# Error   : HTTP status code is not 200(-1)
def get_user_info(str_id):
    print("フォローリクエストしているユーザーの情報を取得します")

    # リクエストに付与するパラメータの作成
    param_id = ",".join(str_id)

    # リクエストに付与するパラメータ
    params = {"user_id":param_id}

    # OAuth認証をし、GETメソッドでユーザー情報の取得
    session = OAuth1Session(myinfo["CK"], myinfo["CS"], myinfo["AT"], myinfo["AS"])
    res = session.get(URL["users_lookup"], params=params)

    # リクエスト情報
    # print(res.status_code)
    # print(res.headers)

    # レスポンスをJSON形式に変換
    userinfo = json.loads(res.text)

    if res.status_code == 200:
        print("<< Succeed!\n")
    # リクエスト失敗
    else:
        print("<< ERROR! : {0}".format(res.status_code))
        return -1

    scr_name_list = list()
    # User IDから取得したScreen Nameの一覧
    print("+----------------------------------------------+")
    print(" Get follow-request user\'s info")
    for (index, name) in enumerate(userinfo):
        scr_name_list.append(name["screen_name"])
        print("{0:<3} : @{1}".format(index + 1, name["screen_name"]))
    print("+----------------------------------------------+")

    return scr_name_list

# フォローリクエストしているユーザーに対してリプライを送る
# Argument : Screen Name list
# Return : None
def reply_follow_request(name_list):
    print("フォローリクエストしているユーザーにリプライを送ります")
    print("+----------------------------------------------+")
    # スクリーンネームのリストから1人ずつリプライする
    for user in name_list:
        # リプライメッセージの作成
        reply_mes = "To :@{0}\nI checked your follow request.\nThank you follow requests.".format(user)

        # リクエストに付与するパラメータ
        params = {"status":reply_mes}

        # OAuth認証をし、POSTメソッドでツイート
        session = OAuth1Session(myinfo["CK"], myinfo["CS"], myinfo["AT"], myinfo["AS"])
        req = session.post(URL["tweet"], params=params)

        # リクエスト情報
        # print(req.status_code)
        # print(req.headers)
        # print(req.text)

        if req.status_code == 200:
            print("<< This message succeed to reply to @{0}!!".format(user))
        # すでに同一のリプライメッセージを送信していた場合
        elif req.status_code == 403:
            print("<< ERROR! : {0}".format(req.status_code))
            print("I wanted to reply to @{0}.".format(user))
            print("But, this reply message already exists the same reply message. :(")
        # リクエスト失敗
        else:
            print("<< ERROR! : {0}".format(req.status_code))

        print("+----------------------------------------------+")

# 自分のタイムラインを取得する
# Argument : None
# Return  : get home timeline(timelines)
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
    timelines = json.loads(res.text)

    if res.status_code == 200:
        print("<< Succeed!")
        for timeline in timelines:
            print("+----------------------------------------------+")
            mes = " @{0}: {1}\n created at {2}\n {3}".format(
                timeline["user"]["screen_name"],
                timeline["user"]["name"],
                timeline["created_at"],
                timeline["text"]
                )
            print(mes)
            # log.append(message)
        print("+----------------------------------------------+")
    # リクエスト失敗
    else:
        print("<< ERROR! : {0}".format(res.status_code))

    return timelines

# 指定したscreen_nameのタイムラインを取得
# Argument : None
# Return  : get target user's timeline(timelines)
def user_timeline():
        print("指定したユーザーのタイムラインを取得します")
        print("@screen_nameを入力してください(@は抜いてね)")
        user = input(termname)
        print("------------------------------------------------")

        # リクエストに付与するパラメータ
        params = {"screen_name":user,
                  "count":50}

        # OAuth認証をし、GETメソッドでユーザーのタイムラインを取得
        session = OAuth1Session(myinfo["CK"], myinfo["CS"], myinfo["AT"], myinfo["AS"])
        res = session.get(URL["user_timeline"], params=params)

        # レスポンスをJSON形式に変換
        timelines = json.loads(res.text)

        if res.status_code == 200:
            print("<< Succeed!")
            for timeline in timelines:
                print("+----------------------------------------------+")
                mes = " @{0}: {1}\n created at {2}\n {3}".format(
                    timeline["user"]["screen_name"],
                    timeline["user"]["name"],
                    timeline["created_at"],
                    timeline["text"]
                    )
                print(mes)
                # log.append(message)
            print("+----------------------------------------------+")
        # リクエスト失敗
        else:
            print("<< ERROR! : {0}".format(res.status_code))

        return timelines

# 指定したユーザーのフォロワーを取得する
# Argument : None
# Return  : get user's followers list(followers)
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
    followers = json.loads(res.text)

    if res.status_code == 200:
        print("<< Succeed!")
        for follower in followers["users"]:
            print("+----------------------------------------------+")
            mes = " @{0}: {1}\n Created at {2}\n Followers: {3}\n Friends: {4}\n Location: {5}\n URL: {6}\n {7} tweet".format(
                follower["screen_name"],
                follower["name"],
                follower["created_at"],
                follower["followers_count"],
                follower["friends_count"],
                follower["location"],
                follower["url"],
                follower["statuses_count"]
                )
            print(mes)
            # log.append(mes)
        print("+----------------------------------------------+")
    # リクエスト失敗
    else:
        print("<< ERROR! : {0}".format(req.status_code))

    return followers

# ツイート内容に対してキーワード検索を行う
# Argument : None
# Return  : get tweets info(tweets)
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
    # リクエスト失敗
    else:
        print("<< ERROR! : {0}".format(req.status_code))

        return tweets

# 地域のトレンドを取得
# Argument : None
# Return  : get target place trends(trends)
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
    trends = json.loads(res.text)

    if res.status_code == 200:
        print("<< Succeed!")
        # 他のJSONと少し違うせいかtrends[0]["trends"]じゃないと取得できない
        for trend in trends[0]["trends"]:
            print("+----------------------------------------------+")
            mes = " Trend: {0}\n URL: {1}\n Volume: {2}".format(
                trend["name"],
                trend["url"],
                trend["tweet_volume"]
                )
            print(mes)
            # log.append(message)
        print("+----------------------------------------------+")
    # リクエスト失敗
    else:
        print("<< ERROR! : {0}".format(res.status_code))

    return trends

# cmd_list_mesを表示する関数
def check_cmd_list():
    print("+------------------------+")
    for s in cmd_list_mes:
        print(s)
    print("+------------------------+")

# 繰り返し実行する関数(このスクリプト内で動かす)
def Pytwitter_main():
    # プログラム終了フラグ
    Escape = False

    for (index, value) in enumerate(cmd_list):
        cmd_list_mes.append(" {0:<2}: {1}".format(index + 1, value))

    print("コマンドリスト")
    check_cmd_list()

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
                str_id = get_follow_requests()
                name_list = get_user_info(str_id)
                reply_follow_request(name_list)
            elif cmd == cmd_list[2]:
                home_timeline()
            elif cmd == cmd_list[3]:
                user_timeline()
            elif cmd == cmd_list[4]:
                followers_list()
            elif cmd == cmd_list[5]:
                search()
            elif cmd == cmd_list[6]:
                place_trend()
            elif cmd == cmd_list[7]:
                if os.name == "nt":
                    os.system("CLS")
                else:
                    os.system("clear")
                check_cmd_list()
            elif cmd == cmd_list[8]:
                Escape = True
        else:
            print("{0}はコマンドじゃないよ".format(cmd))

    print("Thank you for using Pytwitter")
    print("This code is in https://github.com/mryyomutga/Pytwitter")
    print("{0}, Good Bye!!".format(name))

# importされた場合は呼ばれない
if __name__ == '__main__':

    # リクエスト送信用URL
    # Twitterの開発者用のページを参照
    # URL:https://developer.twitter.com/en/docs
    URL = {
        "tweet":"https://api.twitter.com/1.1/statuses/update.json",
        "friendships_incoming":"https://api.twitter.com/1.1/friendships/incoming.json",
        "users_lookup":"https://api.twitter.com/1.1/users/lookup.json",
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
    cmd_list_mes = list()
    cmd_list =("tweet",
               "reply_follow_request",
               "home_timeline",
               "user_timeline",
               "followers_list",
               "search",
               "place_trend",
               "check",         # コマンドリストの確認
               "escape"         # プログラムの終了
               )

    # tweet()
    ## フォローリクエストに対してリプライを送る場合 ##
    # str_id = get_follow_requests()
    # name_list = get_user_info(str_id)
    # reply_follow_request(name_list)
    ##############################################
    # home_timeline()
    # user_timeline()
    # followers_list()
    # search()
    # place_trend()

    # Pytwitterシェルを起動する
    Pytwitter_main()

    # ログに書き出す
    # with open("PytwitterLog.log", "a+", encoding="utf-8") as f:
    #     for l in log:
    #         f.write(l)
