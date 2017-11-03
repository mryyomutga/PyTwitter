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
# Parameter : None
# Return  : None
def tweet():
    # メッセージリスト
    mes_list = list()
    mes_list.append("Pytwitterからの投稿")
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
    res = session.post(URL["tweet"], params=params)

    if res.status_code == 200:
        print("<< Succeed! {0}\n".format(res.headers["status"]))
        # log.append(mes)
    # リクエスト失敗
    else:
        print("<< ERROR! : {0}".format(res.headers["status"]))

# 指定したユーザーの情報を取得する
# Parameter : Screen name(user_name)
# Return  :
# Succeed : get user information(info)
# Error   : HTTP status code is not 200(-1)
def get_user_info(user_name=""):
    print("指定したユーザーの情報を取得します")
    print("------------------------------------------------")
    # screen_nameを受け取っていない場合
    if user_name == "":
        user_name = input(termname + "@")

    # リクエストに付与するパラメータ
    params = {
        "screen_name":user_name
    }

    # OAuth認証をし、GETメソッドでユーザー情報を取得する
    session = OAuth1Session(myinfo["CK"], myinfo["CS"], myinfo["AT"], myinfo["AS"])
    res = session.get(URL["user_show"], params=params)

    info = json.loads(res.text)

    # レスポンス情報(debug)
    # print(res.text)

    if res.status_code == 200:
        print("<< Succeed! {0}\n".format(res.headers["status"]))
        print("+----------------------------------------------+")
        mes = " @{0}: {1}\n Created at {2}\n Location: {3}\n {4}\n Followed {5}\n Following {6}\n {7} tweet\n".format(
            info["screen_name"],
            info["name"],
            info["created_at"],
            info["location"],
            info["description"],
            info["followers_count"],
            info["friends_count"],
            info["statuses_count"]
            )
        # log.append(mes)
        print(mes)
        return info
    # リクエスト失敗
    else:
        print("<< ERROR! : {0}".format(res.headers["status"]))
        return -1

# フォローリクエストの確認とユーザーIDを取得する
# Parameter : None
# Return  :
# Succeed : Response["ids"](User_ID_list)
# Error   : HTTP status code is not 200(-1) or Not follow requests(-2)
def get_follow_request_uid():
    print("フォローリクエストを確認します")
    print("------------------------------------------------")
    params = {
        "cursor":-1,
        "stringify_ids":True
        }

    # OAuth認証をし、GETメソッドでフォローリクエストの取得
    session = OAuth1Session(myinfo["CK"], myinfo["CS"], myinfo["AT"], myinfo["AS"])
    res = session.get(URL["friendships_incoming"], params=params)

    # レスポンスをJSON形式に変換
    str_id = json.loads(res.text)

    if res.status_code == 200:
        print("<< Succeed! {0}".format(res.headers["status"]))
    # リクエスト失敗
    else:
        print("<< ERROR! : {0}".format(res.headers["status"]))
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
# Parameter : User ID list
# Return  :
# Succeed : get user's Screen Name list(scr_name_list)
# Error   : HTTP status code is not 200(-1)
def get_req_user_info(str_id):
    print("フォローリクエストしているユーザーの情報を取得します")
    print("------------------------------------------------")

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
        print("<< Succeed! {0}".format(res.headers["status"]))
    # リクエスト失敗
    else:
        print("<< ERROR! : {0}".format(res.headers["status"]))
        return -1

    scr_name_list = list()
    # User IDから取得したScreen Nameの一覧
    print("+----------------------------------------------+")
    print(" Get follow-request user\'s info")
    for (index, name) in enumerate(userinfo):
        scr_name_list.append(name["screen_name"])
        print(" {0:<3} : @{1}".format(index + 1, name["screen_name"]))
    print("+----------------------------------------------+")

    return scr_name_list

# フォローリクエストしているユーザーに対してリプライを送る
# Parameter : Screen Name list
# Return : None
def reply_follow_request(name_list):
    print("フォローリクエストしているユーザーにリプライを送ります")
    print("+----------------------------------------------+")
    # スクリーンネームのリストから1人ずつリプライする
    for user in name_list:
        # リプライメッセージの作成
        reply_mes = "To :@{0}\nI checked your follow request.\nThanks your follow requests.".format(user)

        # リクエストに付与するパラメータ
        params = {"status":reply_mes}

        # OAuth認証をし、POSTメソッドでツイート
        session = OAuth1Session(myinfo["CK"], myinfo["CS"], myinfo["AT"], myinfo["AS"])
        res = session.post(URL["tweet"], params=params)

        # レスポンス情報
        # print(res.status_code)
        # print(res.headers)
        # print(res.text)

        if res.status_code == 200:
            print("<< {0}\nThis message succeed to reply to @{1}!!".format(res.headers["status"], user))
        # すでに同一のリプライメッセージを送信していた場合
        elif res.status_code == 403:
            print("<< ERROR! : {0}".format(res.headers["status"]))
            print("I wanted to reply to @{0}.".format(user))
            print("But, this reply message already exists the same reply message. :(")
        # リクエスト失敗
        else:
            print("<< ERROR! : {0}".format(res.headers["status"]))

        print("+----------------------------------------------+")

# フォローリクエストしたユーザーをフォローする
# ※フォローリクエストの承認はできない
# Parameter : Screen name list
# Return  : None
def create_friend_FolReq(name_list):
    print("あなたにフォローリクエストをしているユーザーをフォローします")

    for user in name_list:
        params = {"screen_name":user}
        print(user)
        # OAuth認証をし、POSTメソッドでフォローする
        session = OAuth1Session(myinfo["CK"], myinfo["CS"], myinfo["AT"], myinfo["AS"])
        res = session.post(URL["create_friendship"], params=params)

        if res.status_code == 200:
            print("Succeed to follow @{0}".format(user))
        # リクエスト失敗
        else:
            print("<< ERROR! : {0}".format(res.headers["status"]))

# 自分のタイムラインを取得する
# Parameter : None
# Return  :
# Succeed : get home timeline(timelines)
# Error   : HTTP status code is not 200(-1)
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
        print("<< Succeed! {0}".format(res.headers["status"]))
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
        return timelines
    # リクエスト失敗
    else:
        print("<< ERROR! : {0}".format(res.headers["status"]))
        return -1

# 指定したscreen_nameのタイムラインを取得
# Parameter : None
# Return  :
# Succeed : get target user's timeline(timelines)
# Error   : HTTP status code is not 200(-1)
def user_timeline():
        print("指定したユーザーのタイムラインを取得します")
        print("screen_nameを入力してください")
        user = input(termname + "@  ")
        print("------------------------------------------------")

        # リクエストに付与するパラメータ
        params = {
            "screen_name":user,
            "count":50
            }

        # OAuth認証をし、GETメソッドでユーザーのタイムラインを取得
        session = OAuth1Session(myinfo["CK"], myinfo["CS"], myinfo["AT"], myinfo["AS"])
        res = session.get(URL["user_timeline"], params=params)

        # レスポンスをJSON形式に変換
        timelines = json.loads(res.text)

        if res.status_code == 200:
            print("<< Succeed! {0}".format(res.headers["status"]))
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
            return timelines
        # リクエスト失敗
        else:
            print("<< ERROR! : {0}".format(res.headers["status"]))
            return -1

# 指定したユーザーのフォローを取得する
# Parameter : None
# Return  :
# Succeed : get user's friends list(friends)
# Error   : HTTP status code is not 200(-1)
def get_friends():
    print("指定したユーザーの最新のフォローを200人取得します")
    print("screen_nameを入力してください")
    user = input(termname + "@")
    print("------------------------------------------------")

    # リクエストに付与するパラメータ
    params = {
        "screen_name":user,
        "count":200
        }

    # OAuth認証をし、GETメソッドでフォローを取得
    session = OAuth1Session(myinfo["CK"], myinfo["CS"], myinfo["AT"], myinfo["AS"])
    res = session.get(URL["friends_list"], params = params)

    # レスポンスをJSON形式に変換
    friends = json.loads(res.text)
    # レスポンスヘッダの解析(debug)
    # print(res.headers)

    if res.status_code == 200:
        print("<< Succeed! {0}".format(res.headers["status"]))
        for friend in friends["users"]:
            print("+----------------------------------------------+")
            mes = " @{0}: {1}\n Created at {2}\n Friends: {3}\n Followers: {4}\n Location: {5}\n URL: {6}\n {7} tweet".format(
                friend["screen_name"],
                friend["name"],
                friend["created_at"],
                friend["friends_count"],
                friend["followers_count"],
                friend["location"],
                friend["url"],
                friend["statuses_count"]
                )
            print(mes)
            # log.append(mes)
        print("+----------------------------------------------+")
        return friends
    # リクエスト失敗
    else:
        print("<< ERROR! : {0}".format(res.headers["status"]))
        return -1

# 指定したユーザーのフォロワーを50人取得する
# Parameter : None
# Return  :
# Succeed : get user's followers list(followers)
# Error   : HTTP status code is not 200(-1)
def get_followers():
    print("指定したユーザーの最新のフォロワーを50人取得します")
    print("screen_nameを入力してください")
    user = input(termname + "@")
    print("------------------------------------------------")

    # リクエストに付与するパラメータ
    params = {
        "screen_name":user,
        "count":50                  # countはTwitter APIに投げる際、取得人数を指定する(1~200)
        }

    # OAuth認証をし、GETメソッドでフォロワーを取得
    session = OAuth1Session(myinfo["CK"], myinfo["CS"], myinfo["AT"], myinfo["AS"])
    res = session.get(URL["followers_list"], params = params)

    # レスポンスをJSON形式に変換
    followers = json.loads(res.text)

    if res.status_code == 200:
        print("<< Succeed! {0}".format(res.headers["status"]))
        for follower in followers["users"]:
            print("+----------------------------------------------+")
            mes = " @{0}: {1}\n Created at {2}\n Friends: {3}\n Followers: {4}\n Location: {5}\n URL: {6}\n {7} tweet".format(
                follower["screen_name"],
                follower["name"],
                follower["created_at"],
                follower["friends_count"],
                follower["followers_count"],
                follower["location"],
                follower["url"],
                follower["statuses_count"]
                )
            print(mes)
            # log.append(mes)
        print("+----------------------------------------------+")
        return followers
    # リクエスト失敗
    else:
        print("<< ERROR! : {0}".format(res.headers["status"]))
        return -1

# 指定したユーザーの全フォロワーを取得する(非推奨)
# Parameter : None
# Return  :
# Succeed : get user's followers list(followers_list)
# Error   : HTTP status code is not 200(-1)
# Note    : リクエスト制限に関する処理をしていないため、フォロワーがたくさんいるアカウントを指定した場合
#           制限回数に達した状態でリクエストして例外が発生してしまう
def get_all_followers():
    # リクエストにcursorを指定して、どのページの情報をもらうかを制御
    # cursor = -1のとき先頭ページを指定する
    cursor = -1

    print("指定したユーザーの全フォロワーを取得します")
    print("screen_nameを入力してください")
    # 対象とするscreen_nameの入力
    user = input(termname + "@")
    print("------------------------------------------------")

    # 次のページがあるかどうか
    while cursor != "0":
        # リクエストに付与するパラメータ
        params = {
            "screen_name":user,
            "count":200,
            "cursor":cursor
            }

        # OAuth認証をし、GETメソッドで全フォロワーを取得
        session = OAuth1Session(myinfo["CK"], myinfo["CS"], myinfo["AT"], myinfo["AS"])
        res = session.get(URL["followers_list"], params = params)

        # レスポンスをJSON形式に変換
        followers = json.loads(res.text)
        # 先頭ページ返却用変数
        if cursor == -1:
            followers_list = json.loads(res.text)

        if res.status_code == 200:
            print("<< Succeed! {0}".format(res.headers["status"]))
            for follower in followers["users"]:
                print("+----------------------------------------------+")
                mes = " @{0}: {1}\n Created at {2}\n Friends: {3}\n Followers: {4}\n Location: {5}\n URL: {6}\n {7} tweet".format(
                    follower["screen_name"],
                    follower["name"],
                    follower["created_at"],
                    follower["friends_count"],
                    follower["followers_count"],
                    follower["location"],
                    follower["url"],
                    follower["statuses_count"]
                    )
                print(mes)
                # log.append(mes)
            print("+----------------------------------------------+")
            cursor = followers["next_cursor_str"]
        # リクエスト失敗
        else:
            print("<< ERROR! : {0}".format(res.headers["status"]))
            return -1

    return followers_list

# ツイート内容に対してキーワード検索を行う
# Parameter : None
# Return  :
# Succeed : get tweets info(tweets)
# Error   : HTTP status code is not 200(-1)
def search():
    print("検索する内容を入力してください")
    keyword = input(termname)
    print("------------------------------------------------")

    # リクエストに付与するパラメータ
    params = {
        "q":keyword,
        "locale":"ja",
        "result_type":"recent",
        "count":100
        }

    # OAuth認証をし、GETメソッドでキーワード検索
    session = OAuth1Session(myinfo["CK"], myinfo["CS"], myinfo["AT"], myinfo["AS"])
    res = session.get(URL["search"], params = params)

    # レスポンスをJSON形式に変換
    tweets = json.loads(res.text)

    if res.status_code == 200:
        print("<< Succeed! {0}".format(res.headers["status"]))
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
        return tweets
    # リクエスト失敗
    else:
        print("<< ERROR! : {0}".format(res.headers["status"]))
        return -1

# 地域のトレンドを取得する
# Parameter : None
# Return  :
# Succeed : get target place trends(trends)
# Error   : HTTP status code is not 200(-1)
def place_trend():
    print("地域を指定してください")
    place = input(termname)
    print("------------------------------------------------")

    # リクエストに付与するパラメータ
    params = {
        "id":place_code[place]["woeid"]
        }

    # OAuth認証をし、GETメソッドで地域のトレンドを取得
    session = OAuth1Session(myinfo["CK"], myinfo["CS"], myinfo["AT"], myinfo["AS"])
    res = session.get(URL["place_trend"], params=params)

    # レスポンスをJSON形式に変換
    trends = json.loads(res.text)

    if res.status_code == 200:
        print("<< Succeed! {0}".format(res.headers["status"]))
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
        return trends
    # リクエスト失敗
    else:
        print("<< ERROR! : {0}".format(res.headers["status"]))
        return -1

# プロフィールを変更する
# Parameter : None
# Return  :
# Succeed : get changed profile(prof)
# Error   : HTTP status code is not 200(-1)
def change_profile():
    # 変更するパラメータセット
    change_prof = {
        "name":"",
        "url":"",
        "location":"",
        "description":""
        }
    # 自分のscreen nameを指定してプロフィールを取得する
    myprof = get_user_info(myinfo["screen_name"])

    # get_user_infoでリクエストが失敗していた場合
    if myprof == -1:
        return -1

    print("プロフィールを変更します")
    print("変更しない場合は入力せずEnterキーを押してください")
    print("URLは\"http://\"まで省略可能です")

    # 変更するパラメータの入力
    change_prof["name"]        = input(" Name        " + myprof["name"] + " >> ")
    change_prof["url"]         = input(" URL         " + myprof["url"] + " >> ")
    change_prof["location"]    = input(" Location    " + myprof["location"] + " >> ")
    change_prof["description"] = input(" Description " + myprof["description"] + "\n >> ")
    print("------------------------------------------------")

    # 変更があったかを調べる
    for key, value in change_prof.items():
        # 変更がない場合、取得してあるmyprofの値をセットする
        if value == "":
            change_prof[key] = myprof[key]
        # print(change_prof[key])

    # リクエストに付与するパラメータ
    params = {
        "name":change_prof["name"],
        "url":change_prof["url"],
        "location":change_prof["location"],
        "description":change_prof["description"],
        "include_entities":True,
        "skip_status":False
    }

    # OAuth認証をし、POSTメソッドで変更する属性をAPIに投げる
    session = OAuth1Session(myinfo["CK"], myinfo["CS"], myinfo["AT"], myinfo["AS"])
    res = session.post(URL["update_profile"], params=params)

    # レスポンスをJSON形式に変換
    prof = json.loads(res.text)

    if res.status_code == 200:
        print("<< Succeed! {0}".format(res.headers["status"]))
        print("+----------------------------------------------+")
        mes = " Name: {0}\n URL: {1}\n Location: {2}\n {3}".format(
            prof["name"],
            prof["url"],
            prof["location"],
            prof["description"]
            )
        print(mes)
        # log.append(message)
        print("+----------------------------------------------+")
        return prof
    # リクエスト失敗
    else:
        print("<< ERROR! : {0}".format(res.headers["status"]))
        return -1

# Twitter APIのレートリミットを確認する
def check_rate_limit():
    print("あなたのTwitter APIのレートリミットを取得します")

    # OAuth認証をし、GETメソッドで地域のトレンドを取得
    session = OAuth1Session(myinfo["CK"], myinfo["CS"], myinfo["AT"], myinfo["AS"])
    res = session.get(URL["rate_limit_status"])

    if res.status_code == 200:
        print("<< Succeed! {0}".format(res.headers["status"]))
        # ファイルにレートリミットを書き込む
        # with open("Rate_limit.json", "w") as f:
        #     f.write(res.text)
        print(res.text)
    # リクエスト失敗
    else:
        print("<< ERROR! : {0}".format(res.headers["status"]))

# cmd_list_mesを表示する関数
def check_cmd_list():
    print("+------------------------+")
    for s in cmd_list_mes:
        print(s)
    print("+------------------------+")

# コンソール画面の消去
def console_clear():
    # OSの判定
    if os.name == "nt":
        os.system("CLS")
    else:
        os.system("clear")

# 繰り返し実行する関数(このスクリプト内で動かす)
def Pytwitter_main():
    # プログラム終了フラグ
    Escape = False
    console_clear()

    for (index, value) in enumerate(cmd_list):
        cmd_list_mes.append(" {0:<2}: {1}".format(index + 1, value))

    print("コマンドリスト")
    check_cmd_list()

    # Pytwitterの起動
    while Escape == False:
        print("何をしますか?")
        cmd = input(termname)
        # 入力されたコマンドがリストに存在するか
        if cmd in cmd_list or cmd == "":
            console_clear()
            # コマンドの実行
            if cmd == cmd_list[0]:
                tweet()
            elif cmd == cmd_list[1]:
                get_user_info()
            elif cmd == cmd_list[2]:
                str_id = get_follow_request_uid()
                name_list = get_req_user_info(str_id)
                reply_follow_request(name_list)     # 相手に見えないため意味なし
                # create_friend_FolReq(name_list)
            elif cmd == cmd_list[3]:
                home_timeline()
            elif cmd == cmd_list[4]:
                user_timeline()
            elif cmd == cmd_list[5]:
                get_friends()
            elif cmd == cmd_list[6]:
                get_followers()
            elif cmd == cmd_list[7]:
                get_all_followers()
            elif cmd == cmd_list[8]:
                search()
            elif cmd == cmd_list[9]:
                place_trend()
            elif cmd == cmd_list[10]:
                change_profile()
            elif cmd == cmd_list[11]:
                check_cmd_list()
            elif cmd == cmd_list[12]:
                Escape = True
        else:
            print("{0}はコマンドじゃないよ".format(cmd))

    print("Thank you for using \033[33mPytwitter\033[0m")
    print("This script is in \033[32mhttps://github.com/mryyomutga/Pytwitter\033[0m")
    print("{0}, Good Bye!!".format(name))

# importされた場合は呼ばれない
if __name__ == '__main__':
    # リクエストするAPIのURL
    # Twitterの開発者用のページを参照
    # URL:https://developer.twitter.com/en/docs
    URL = {
        "tweet":"https://api.twitter.com/1.1/statuses/update.json",
        "friendships_incoming":"https://api.twitter.com/1.1/friendships/incoming.json",
        "user_show":"https://api.twitter.com/1.1/users/show.json",
        "users_lookup":"https://api.twitter.com/1.1/users/lookup.json",
        "create_friendship":"https://api.twitter.com/1.1/friendships/create.json",
        "home_timeline":"https://api.twitter.com/1.1/statuses/home_timeline.json",
        "user_timeline":"https://api.twitter.com/1.1/statuses/user_timeline.json",
        "friends_list":"https://api.twitter.com/1.1/friends/list.json",
        "followers_list":"https://api.twitter.com/1.1/followers/list.json",
        "search":"https://api.twitter.com/1.1/search/tweets.json",
        "place_trend":"https://api.twitter.com/1.1/trends/place.json",
        "update_profile":"https://api.twitter.com/1.1/account/update_profile.json",
        "rate_limit_status":"https://api.twitter.com/1.1/application/rate_limit_status.json"
    }
    # ログを確保するリスト
    # log = list()

    # TwitterAPIKey.jsonからConsumer keyやAccess tokenを読み出し
    with open("TwitterAPIKey.json", "r", encoding="utf-8") as f:
        myinfo = json.load(f)

    # 地域情報取得用WOEIDの読み出し(日本のみ)
    # URL:https://shun1adhocblog.wordpress.com/2013/01/01/twitterapi%E3%82%92%E4%BD%BF%E3%81%A3%E3%81%A6%E3%81%BF%E3%82%8B%E3%83%86%E3%82%B9%E3%83%88by-python/
    with open("woeid.json", "r", encoding="utf-8") as f:
        place_code = json.load(f)

    # アカウント名を表示する場合
    name = "\033[36m@" + myinfo["screen_name"] + "\033[0m"
    termname = name + " >> "
    # termname = ">> "

    # コマンドリスト
    cmd_list_mes = list()
    cmd_list =("tweet",
               "get_user_info",
               "reply_follow_request",
               "home_timeline",
               "user_timeline",
               "get_friends",
               "get_followers",
               "get_all_followers",
               "search",
               "place_trend",
               "change_profile",
               "check",         # コマンドリストの確認
               "escape"         # プログラムの終了
               )

    # tweet()
    ## フォローリクエストに対してリプライを送る場合 ##
    # str_id = get_follow_request_uid()
    # name_list = get_req_user_info(str_id)
    # reply_follow_request(name_list)
    ##############################################
    # home_timeline()
    # user_timeline()
    # get_followers_list()
    # search()
    # place_trend()

    Pytwitter_main()

    # ログに書き出す
    # with open("PytwitterLog.log", "a+", encoding="utf-8") as f:
    #     for l in log:
    #         f.write(l)
