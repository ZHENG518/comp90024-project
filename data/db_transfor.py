import json
import couchdb

db_ip = '172.26.133.160'
db_name = 'aurin_language_data'
couchdb_server = couchdb.Server(f'http://admin:password@{db_ip}:5984')
with open('./language_data.json', 'r') as f:
    data = json.load(f)

try:
    db = couchdb_server[db_name] # 使用已经存在的数据库
except:
    db = couchdb_server.create(db_name) # 新建数据库

db.save(data)
