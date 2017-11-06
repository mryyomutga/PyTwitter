# -*- coding: utf-8 -*-
# Name      : Bot.py
# Author    : Ryoga Miyamoto
# Outline   : node.jsでBot
# Env       : Python3.6.3
# Repository: https://github.com/mryyomutga/PyTwitter

# Python2でPython3のprint()を使用するモジュール
from __future__ import print_function
# Requests,OAuth認証用ライブラリ(requestsモジュールから派生)
from requests_oauthlib import OAuth1Session
# json形式データを扱うライブラリ
import json
# 画面消去するCLS、clearを呼び出す
import os
import sys

def bot(arg):

    s = "test node.js local server run:{0}".format(arg)
    # リクエストに付与するパラメータ
    params = {"status":s}

    # POSTメソッドでツイート
    res = session.post(URL["tweet"], params=params)

    if res.status_code == 200:
        print("<< Succeed! {0}".format(res.headers["status"]))
    # リクエスト失敗
    else:
        print("<< ERROR! : {0}".format(res.headers["status"]))


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
    with open("MyTwitterAPIKey.json", "r", encoding="utf-8") as f:
        myinfo = json.load(f)

    # 地域情報取得用WOEIDの読み出し(日本のみ)
    # URL:https://shun1adhocblog.wordpress.com/2013/01/01/twitterapi%E3%82%92%E4%BD%BF%E3%81%A3%E3%81%A6%E3%81%BF%E3%82%8B%E3%83%86%E3%82%B9%E3%83%88by-python/
    with open("woeid.json", "r", encoding="utf-8") as f:
        place_code = json.load(f)

    # アカウント名を表示する場合
    name = "\033[36m@" + myinfo["screen_name"] + "\033[0m"
    termname = name + " >> "
    # termname = ">> "

    # 取得したキーに対してOAuth認証をする
    session = OAuth1Session(myinfo["CK"], myinfo["CS"], myinfo["AT"], myinfo["AS"])

    args = sys.argv
    bot(args[1])
    
