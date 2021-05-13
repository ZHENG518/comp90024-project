from tweepy import OAuthHandler, Stream, StreamListener
import tweepy
import json
import emoji
import couchdb
import re

db_ip = 'localhost'
db_name = 'twitter'
couchdb_server = couchdb.Server(f'http://admin:password@{db_ip}:5984')

try:
    db = couchdb_server[db_name] # 使用已经存在的数据库
except:
    db = couchdb_server.create(db_name) # 新建数据库

consumer_key = '2fMtwWMayWv6KGj4S9YP6nP1r'
consumer_secret = 'JnEuZbKhkmPRkpN2r7QmezKHi1l6cSNQ3GhSXqM6ag0KaH3PQ4'
access_token = '1384380289187786753-7kFtEmVjCL8tg4Nz4K69kW7mEQwhnL'
access_token_secret = 'w6KraDeDPV8uG8kh2fwmrWtnDLzO4MYA6o8fr4D1QwNmS'
melbourne_bouning_box = [144.33363404800002, -38.50298801599996, 145.8784120140001, -37.17509899299995]
Australia_bouning_box = [112.921114, -43.740482, 159.109219, -9.142176]
mel_place_id = '01864a8a64df9dc4'

aurin_db = couchdb_server['aurin_language_data']
id = list(aurin_db)[0]
region_dta = dict(aurin_db[id])

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
    for block in region_dta['features']:
        if point_check_inside(coordinates["coordinates"][0], coordinates["coordinates"][1], block['geometry']['coordinates'][0][0]):
            return block['properties']['name']
    return None


def loadDictionary():
    slang_wordDict = dict()
    words_All = []
    with open('../resources/slang.txt','r', encoding='UTF-8') as slang_file:
        for line in slang_file:
            word=line.split(' ')
            #slang_wordDict.append(word[0].lower())
            slang_wordDict[word[0].lower()]=0
            words_All.append(word[0].lower())
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

    # # streaming api
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

