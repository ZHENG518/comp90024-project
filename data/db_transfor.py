import json
import couchdb

# db_ip = '172.26.133.160'
db_ip='localhost'
db_name = 'aurin_data'
couchdb_server = couchdb.Server(f'http://admin:password@{db_ip}:5984')


try:
    db = couchdb_server[db_name] # 使用已经存在的数据库
except:
    db = couchdb_server.create(db_name) # 新建数据库


# with open('./language_data.json', 'r') as f:
#     language_data = json.load(f)
# db['language_data'] = language_data
#
# with open('./cities_data.json', 'r') as f:
#     cities_data = json.load(f)
# db['cities_data'] = cities_data

with open('./covid_cases.json', 'r') as f:
    covid_cases = json.load(f)
db['covid_cases'] = covid_cases