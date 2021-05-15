import tweepy
import couchdb
import nltk
import re
nltk.download('vader_lexicon')
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from pyspark import SparkContext, SparkConf
import time
from api_keys import *
import os

conf = SparkConf().setAppName("covid-19").setMaster("local[*]")
sc=SparkContext.getOrCreate(conf)

# 提交你的Key和secret
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

# 获取类似于内容句柄的东西
api = tweepy.API(auth)

vader = SentimentIntensityAnalyzer()

db_ip = os.environ.get('DATABASE_IP','localhost')
couch = couchdb.Server(f'http://admin:password@{db_ip}:5984')
db_name = 'twitter_covid'
try:
    db = couch[db_name]  # 使用已经存在的数据库
except:
    db = couch.create(db_name)  # 新建数据库
    db = couch[db_name]


def calculate_emotion(tweet, location):
    tweet = tweet._json
    text = tweet["text"]
    text_cut_link = re.sub(
        r'\s(https?)?(:\/\/)?(www\.)?[-a-zA-Z0-9@:%._\+~#=0-9]{1,256}\.[-a-zA-Z0-9@:%_\+.~#?&//=]*\b', '', text)
    text_final = re.sub(r'\@[\w]*', '', text_cut_link)
    scores = vader.polarity_scores(text_final)
    tweet["compound"] = scores["compound"]
    tweet["c_location"] = location
    if tweet["compound"] > 0:
        tweet["emotion"] = "pos"
    elif tweet["compound"] < 0:
        tweet["emotion"] = "neg"
    else:
        tweet["emotion"] = "neu"
    db.save(tweet)
    # print(scores)


def calculate_Melbourne():
    # mel_place_id='01864a8a64df9dc4'
    # API.search(q, *, geocode, lang, locale, result_type, count, until, since_id, max_id, include_entities)
    all_tweets = tweepy.Cursor(api.search, q="covid-19", geocode="-37.85,145.12,80km", lang="en", count=100).pages(50)
    for tweet_part in all_tweets:
        rdd = sc.parallelize(tweet_part, 12)
        # print("rdd: {}".format(rdd))
        rdd1 = rdd.map(lambda x: calculate_emotion(x, "Melbourne")).collect()
        print(len(rdd1))
        # print("rdd1: {}".format(rdd1))


def calculate_Sydney():
    # API.search(q, *, geocode, lang, locale, result_type, count, until, since_id, max_id, include_entities)
    all_tweets = tweepy.Cursor(api.search, q="covid-19", geocode="-33.7,151,80km", lang="en", count=100).pages(50)
    for tweet_part in all_tweets:
        rdd = sc.parallelize(tweet_part, 12)
        # print("rdd: {}".format(rdd))
        rdd1 = rdd.map(lambda x: calculate_emotion(x, "Sydney")).collect()
        print(len(rdd1))
        # print("rdd1: {}".format(rdd1))


def calculate_Canberra():
    # API.search(q, *, geocode, lang, locale, result_type, count, until, since_id, max_id, include_entities)
    all_tweets = tweepy.Cursor(api.search, q="covid-19", geocode="-35.29,149.12,30km", lang="en", count=100).pages(50)
    for tweet_part in all_tweets:
        rdd = sc.parallelize(tweet_part, 12)
        # print("rdd: {}".format(rdd))
        rdd1 = rdd.map(lambda x: calculate_emotion(x, "Canberra")).collect()
        print(len(rdd1))
        # print("rdd1: {}".format(rdd1))


def calculate_Brisbane():
    # API.search(q, *, geocode, lang, locale, result_type, count, until, since_id, max_id, include_entities)
    all_tweets = tweepy.Cursor(api.search, q="covid-19", geocode="-27.43,152.91,60km", lang="en", count=100).pages(50)
    for tweet_part in all_tweets:
        rdd = sc.parallelize(tweet_part, 12)
        # print("rdd: {}".format(rdd))
        rdd1 = rdd.map(lambda x: calculate_emotion(x, "Brisbane")).collect()
        print(len(rdd1))
        # print("rdd1: {}".format(rdd1))


if __name__ == '__main__':
    start = time.time()
    calculate_Melbourne()
    calculate_Sydney()
    calculate_Canberra()
    calculate_Brisbane()
    end = time.time()
    print(end - start)