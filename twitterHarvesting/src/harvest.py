from tweepy import OAuthHandler, Stream, StreamListener
import os
import tweepy
import json
import emoji
import couchdb
import re

# db_ip = os.environ.get('DATABASE_IP','localhost')
db_ip = '172.26.132.26'
db_name = 'twitter'
couchdb_server = couchdb.Server(f'http://admin:password@{db_ip}:5984')

try:
    db = couchdb_server[db_name] # 使用已经存在的数据库
except:
    db = couchdb_server.create(db_name) # 新建数据库

consumer_key = 'Xm8NLd2HVSpcwZh94FRMhp8zK'
consumer_secret = 'tokpqJFu9wa54soHkYvq2QSWGEDLNzmREaGS1InkfgwuCE9xdZ'
access_token = '1384380289187786753-aEOI10FGgKGlejbL3hObtvLHU9pgQ9'
access_token_secret = 'jfRPnUHDfUKVDmcOuJKKLwyn9semcZRb06oWeXDKV318g'
Australia_bouning_box = [112.921114, -43.740482, 159.109219, -9.142176]
mel_place_id = '01864a8a64df9dc4'

# aurin_db = couchdb_server['aurin_data']
aurin_db = couchdb.Server(f'http://admin:password@localhost:5984')['aurin_data']
region_data = dict(aurin_db['language_data'])

def point_check_inside(lng, lat, polygon):
    num = len(polygon) - 1
    int_point = 0
    for i in range(num):
        if polygon[i][1] == polygon[i + 1][1]:
            if polygon[i][1] == lat:
                return False
        if ((polygon[i][1] < lat and lat < polygon[i + 1][1]) or (polygon[i + 1][1] < lat and lat < polygon[i][1])):
            xseg = polygon[i][0] + (polygon[i + 1][0] - polygon[i][0]) * (lat - polygon[i][1]) / (
                        polygon[i + 1][1] - polygon[i][1])  # 求交
            if lng < xseg:
                int_point += 1
    if int_point % 2 == 1:
        return True
    else:
        return False

    # Fetch polygon parameter from json file
def append_attribute(coordinates):
    if not coordinates:
        return None
    for block in region_data['features']:
        if point_check_inside(coordinates["coordinates"][0], coordinates["coordinates"][1], block['geometry']['coordinates'][0][0]):
            return block['properties']['name']
    return None


def loadDictionary():
    words_All = []
    with open('../resources/internet_slangs.txt','r', encoding='UTF-8') as slang_file:
        for line in slang_file.readlines():
            word=line.strip('\n')
            words_All.append(word.lower())
    regex="|".join(words_All)
    return regex

slang_pattern = loadDictionary()
def calculate_slang(text):
    text = text.lower()
    result_findall = re.findall(r"\b(%s)\b" %slang_pattern, text)
    return result_findall


def calculate_emoji(text):
    emoji_all = []
    pro_text = emoji.demojize(text)
    #print(pro_text)
    emoji_result = re.findall(r"(:[a-zA-Z_-]+:)" , pro_text)
    emoji_result = list(set(emoji_result))
    for each_emoji in emoji_result:
        emoji_i = emoji.emojize(each_emoji)
        emoji_all.append(emoji_i)
    return emoji_all

def generate_document(tweet_data):
    tweet_text = tweet_data['text']
    tweet_data["emoji"] = calculate_emoji(tweet_text)
    tweet_data["slang"] = calculate_slang(tweet_text)
    tweet_data['melb_SA3_name'] = append_attribute(tweet_data["coordinates"])
    return tweet_data

class StdOutListener(StreamListener):
    def on_data(self, data):
        tweet_data = json.loads(data)
        id_str = tweet_data['id_str']
        if id_str not in db:
            document = generate_document(tweet_data)
            db[id_str] = document
            print(document)
        else:
            print(id_str+' already in the database')
        return True

    def on_error(self, status):
        print(status)

if __name__ == '__main__':
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)

    # streaming api
    # l = StdOutListener()
    # stream = Stream(auth, l)
    # stream.filter(locations=Australia_bouning_box)

    # search api
    api = tweepy.API(auth)
    all_tweets = tweepy.Cursor(api.search,q="place:%s" % mel_place_id,count = 100).pages(100000)
    for tweet_part in all_tweets:
        for tweet in tweet_part:
            tweet_data =tweet._json
            id_str = tweet_data['id_str']
            if id_str not in db:
                document = generate_document(tweet_data)
                db[id_str] = document
                print(document)
            else:
                print(id_str + ' already in the database')

