import os
from flask import Flask, jsonify, request, g
from flask_cors import CORS
from resources import lag_code_map
import couchdb

db_ip = os.environ.get('DATABASE_IP','localhost')
db_name = 'twitter'
db_server = couchdb.Server(f'http://admin:password@{db_ip}:5984')

aurin_db = db_server['aurin_data']
# aurin_db = couchdb.Server(f'http://admin:password@localhost:5984')['aurin_data']
twitter_db = db_server['twitter']
covid_db = db_server['twitter_covid']

app = Flask(__name__)
CORS(app, supports_credentials=True)

@app.route('/basic_stats', methods=['GET'])
def basic_stats():
    try:
        language_count_view = twitter_db.view('basic_stats/language_count', reduce='true', group_level='1')
        language_count = []
        others_count = 0
        for row in language_count_view.rows:
            if row.key[0] in lag_code_map:
                language_count.append({'name': lag_code_map.get(row.key[0]), 'value': row.value})
            else:
                others_count += row.value
        language_count.append({'name':'others','value':others_count})

        hashtag_count_view = twitter_db.view('basic_stats/hashtag_count', reduce='true', group_level='1')
        hashtag_count = []
        for row in hashtag_count_view.rows:
            hashtag_count.append({'name':'#'+row.key[0], 'value':row.value})

        emoji_count_view = twitter_db.view('basic_stats/emoji_count', reduce='true', group_level='1')
        emoji_count = []
        for row in emoji_count_view.rows:
            emoji_count.append({'name':row.key[0], 'value':row.value})

        slang_count_view = twitter_db.view('basic_stats/slang_count', reduce='true', group_level='1')
        slang_count = []
        for row in slang_count_view.rows:
            slang_count.append({'name':row.key[0], 'value':row.value})


        return jsonify({
            'code': 1000,
            'data':{
                'total_counts': len(twitter_db),
                'language_count': sorted(language_count, key=lambda item:item['value'], reverse=True),
                'hashtag_count': sorted(hashtag_count, key=lambda item:item['value'], reverse=True)[:50],
                'emoji_count':sorted(emoji_count, key=lambda item:item['value'], reverse=True)[:100],
                'slang_count': sorted(slang_count, key=lambda item:item['value'], reverse=True)[:100]
            }
        })
    except Exception as e:
        return jsonify({'code': 2000, 'message': e})


@app.route('/language_data', methods=['GET'])
def language_data():
    aurin_data = dict(aurin_db['language_data'])
    del aurin_data['_id']
    del aurin_data['_rev']

    language_count_view = twitter_db.view('basic_stats/suburb_language', reduce='true', group_level='1')
    language_count = {}
    for row in language_count_view.rows:
        language_count[lag_code_map.get(row.key[0],'others')] = row.value

    suburb_language_view = twitter_db.view('basic_stats/suburb_language', reduce='true', group_level='2')
    suburb_language = {}
    for row in suburb_language_view.rows:
        language = lag_code_map.get(row.key[0],'others')
        suburb = row.key[1]
        suburb_dict = suburb_language.get(suburb, dict())
        suburb_dict[language + '_tweets'] = row.value
        suburb_dict[language + '_tweets_percentage'] = float('%.4f' % (row.value / language_count[language]))
        suburb_language[suburb] = suburb_dict

    all_zero = {}
    for language in lag_code_map.values():
        all_zero[language+ '_tweets'] = 0
        all_zero[language+ '_tweets_percentage'] = 0

    for feature in aurin_data['features']:
        suburb = feature['properties']['name']
        feature['properties'].update(all_zero)
        if suburb in suburb_language:
            feature['properties'].update(suburb_language[suburb])

    return jsonify({
        'code':1000,
        'data':aurin_data
    })

@app.route('/covid_data', methods=['GET'])
def covid_data():
    aurin_data = dict(aurin_db['cities_data'])
    del aurin_data['_id']
    del aurin_data['_rev']

    emotion_count_view = covid_db.view('emotion_analyse/emotion_count', reduce='true', group_level='2')
    emotion_count = {}
    for row in emotion_count_view.rows:
        city = row.key[0]
        city_dict = emotion_count.get(city, {})
        city_dict[row.key[1]] = row.value
        emotion_count[city] = city_dict

    emotion_score_view = covid_db.view('emotion_analyse/emotion_average', reduce='true', group_level='1')
    emotion_score = {}
    for row in emotion_score_view.rows:
        emotion_score[row.key] = float('%.4f' % (row.value))

    city_map = {'Greater Sydney': 'Sydney', 'Greater Melbourne': 'Melbourne',
                'Greater Brisbane': 'Brisbane', 'Australian Capital Territory': 'Canberra'}
    for feature in aurin_data['features']:
        city_name = city_map[feature['properties']['city_name']]
        feature['properties']['score'] = emotion_score[city_name]
        feature['properties'].update(emotion_count[city_name])

    return jsonify({
        'code':1000,
        'data':aurin_data
    })

@app.route('/covid_cases', methods=['GET'])
def covid_cases():
    aurin_data = dict(aurin_db['covid_cases'])

    return jsonify({
        'code': 1000,
        'data': aurin_data
    })


@app.route('/test', methods=['GET'])
def test():
    try:
        return jsonify({
            'code': 1000,
            'data': f'Backend deploy successfully! Database IP: {db_ip}'
        })
    except Exception as e:
        return jsonify({'code': 2000, 'message': e})

if __name__ == '__main__':
    app.run(host="0.0.0.0")