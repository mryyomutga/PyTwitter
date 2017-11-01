# -*- coding: utf-8 -*-
# Pytwitter.py
# Author    : Ryoga Miyamoto
from requests_oauthlib import OAuth1Session
import json

# リクエスト送信用URL
URL = {
        "tweet":"https://api.twitter.com/1.1/statuses/update.json",
        "search":"https://api.twitter.com/1.1/search/tweets.json"
}

# TwitterAPIKey.jsonからTwitterAPIの読み出し
with open("TwitterAPIKey.json", "r") as f:
    apiKey = json.load(f)

# Tweetを行う
def tweet():
    # ツイートフォーム
    message = list()
    print("つぶやく内容を入力してください(-qで入力終了)")
    message.append(input(">> "))
    while message[-1] != "-q":
        message.append(input(">> "))
    print("------------------------------------------------")

    message.pop()
    mes = "\n".join(message)
    print(mes)
    params = {"status":mes}
    # OAuth認証をし、POSTリクエストでツイート
    session = OAuth1Session(apiKey["CK"], apiKey["CS"], apiKey["AT"], apiKey["AS"])
    req = session.post(URL["tweet"], params=params)

    if req.status_code == 200:
        print("<< Succeed!")
        print(message)
        log.append(message)
    else:
        print("<< ERROR! : {0}".format(req.status_code))

def research():
    global log
    print("検索する内容を入力してください")
    keyword = input(">> ")
    params = {"q":keyword,
              "locale":"ja",
              "result_type":"recent",
              "count":50}

    # OAuth認証をし、GETリクエストで検索
    session = OAuth1Session(apiKey["CK"], apiKey["CS"], apiKey["AT"], apiKey["AS"])
    res = session.get(URL["search"], params = params)

    # レスポンスをJSON形式に変換
    tweets = json.loads(res.text)

    if res.status_code == 200:
        print("<< Succeed!\n")
        for tweet in tweets["statuses"]:
            mes = "@{0}: {1}\nDate: {2}\n{3}\n".format(
                tweet["user"]["screen_name"],
                tweet["user"]["name"],
                tweet["created_at"],
                tweet["text"]
                )
            print(mes)
            with open("tweet.json", "w", encoding="cp932") as f:
                f.write(json.dumps(tweet))

            log.append(mes)
    else:
        print("<< ERROR! : {0}".format(req.status_code))

# 取得したツイートのログリスト
log = list()

tweet()
# research()

# with open("PytwitterLog.log", "a+", encoding="utf-8") as f:
#     for l in log:
#         f.write(l)
