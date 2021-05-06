import couchdb

couch = couchdb.Server('http://admin:password@172.26.133.160:5984')
db = couch['test_twitter']

views = {
    "get_language":{
        "map":"""function (doc) {
                    emit([doc.user.lang, doc.user.time_zone], 1);
                  }""",
        "reduce":"_stats"
    }
}

db['_design/example'] = dict(language='javascript', views=views)

result = db.view('example/get_language', reduce='true', group_level='2')
