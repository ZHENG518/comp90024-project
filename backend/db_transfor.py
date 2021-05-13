import couchdb
import json

# db_ip = '172.26.133.160'
# db_name = 'test_twitter'
# design_doc_name = 'basic_stats'
#
#
# couch = couchdb.Server(f'http://admin:password@{db_ip}:5984')

with open('../data/SA3-language.json', 'r') as f:
    data = json.load(f)
print('aaa')