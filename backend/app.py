import os
from flask import Flask, jsonify, request, g
from flask_cors import CORS
from resources import lag_code_map
import couchdb

db_ip = os.environ.get('DATABASE_IP','localhost')
db_name = 'twitter'
db_server = couchdb.Server(f'http://admin:password@{db_ip}:5984')

app = Flask(__name__)
CORS(app, supports_credentials=True)

@app.route('/basic_stats', methods=['GET'])
def basic_stats():
    try:
        couchdb_instance = db_server[db_name]
        language_count_view = couchdb_instance.view('basic_stats/language_count', reduce='true', group_level='1')
        language_count = []
        for row in language_count_view.rows:
            if row.key[0] in lag_code_map:
                language_count.append({'name':lag_code_map.get(row.key[0]),'value':row.value})

        hashtag_count_view = couchdb_instance.view('basic_stats/hashtag_count', reduce='true', group_level='1')
        hashtag_count = []
        for row in hashtag_count_view.rows:
            hashtag_count.append({'name':'#'+row.key[0], 'value':row.value})

        emoji_count_view = couchdb_instance.view('basic_stats/emoji_count', reduce='true', group_level='1')
        emoji_count = []
        for row in emoji_count_view.rows:
            emoji_count.append({'name':row.key[0], 'value':row.value})

        slang_count_view = couchdb_instance.view('basic_stats/slang_count', reduce='true', group_level='1')
        slang_count = []
        for row in slang_count_view.rows:
            slang_count.append({'name':row.key[0], 'value':row.value})


        return jsonify({
            'code': 1000,
            'data':{
                'total_counts': len(couchdb_instance),
                'language_count': sorted(language_count, key=lambda item:item['value'], reverse=True),
                'hashtag_count': sorted(hashtag_count, key=lambda item:item['value'], reverse=True)[:50],
                'emoji_count':sorted(emoji_count, key=lambda item:item['value'], reverse=True)[:50],
                'slang_count': sorted(slang_count, key=lambda item:item['value'], reverse=True)[:50]
            }
        })
    except Exception as e:
        return jsonify({'code': 2000, 'message': e})


@app.route('/language_data', methods=['GET'])
def language_data():
    db = db_server['aurin_language_data']
    id = list(db)[0]
    aurin_data = dict(db[id])
    del aurin_data['_id']
    del aurin_data['_rev']

    couchdb_instance = db_server[db_name]
    language_count_view = couchdb_instance.view('basic_stats/suburb_language', reduce='true', group_level='1')
    language_count = {}
    for row in language_count_view.rows:
        if row.key[0] in lag_code_map:
            language_count[lag_code_map[row.key[0]]] = row.value

    suburb_language_view = couchdb_instance.view('basic_stats/suburb_language', reduce='true', group_level='2')
    suburb_language = {}
    for row in suburb_language_view.rows:
        language = lag_code_map[row.key[0]]
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


@app.route('/test', methods=['GET'])
def test():
    try:
        name = request.args.get("name")
        return jsonify({
            'code': 1000,
            'data': f'Backend deploy successfully! Database IP: {db_ip}'
        })
    except Exception as e:
        return jsonify({'code': 2000, 'message': e})

if __name__ == '__main__':
    app.run(host="0.0.0.0")