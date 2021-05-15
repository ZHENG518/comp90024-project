import couchdb

db_ip = 'localhost'
couch = couchdb.Server(f'http://admin:password@{db_ip}:5984')

# couchdb views for scenario1，2
db_name = 'twitter'
design_doc_name = 'basic_stats'
db = couch[db_name]

basic_stats_views = {
    "language_count":{
        "map":"""function (doc) {
                    if (doc.lang != 'und'){
                        emit([doc.lang], 1);
                    }
                }""",
        "reduce":"_count"
    },
    "hashtag_count":{
        "map":"""function (doc) {
                    doc.entities.hashtags.forEach(function (item) {
                        emit([item.text], 1);
                    });
                  }""",
        "reduce":"_count"
    },
    "emoji_count":{
        "map":"""function (doc) {
                    doc.emoji.forEach(function (item) {
                        emit([item], 1);
                    });
                  }""",
        "reduce":"_count"
    },
    "slang_count": {
        "map": """function (doc) {
                doc.slang.forEach(function (item) {
                    emit([item], 1);
                });
              }""",
        "reduce": "_count"
    },
    "suburb_language":{
        "map": """function (doc) {
                    if (doc.melb_SA3_name !== null && doc.lang != 'und'){
                        emit([doc.lang, doc.melb_SA3_name,],1);
                    }
                }""",
        "reduce": "_count"
    }
}

db[f'_design/{design_doc_name}'] = dict(language='javascript', views=basic_stats_views)

# couchdb views for scenario 3
db = couch['twitter_covid']

views = {
    "emotion_count": {
        "map": """function (doc) {
                    emit([doc.c_location,doc.emotion],1);
                  }""",
        "reduce": "_sum"
    },
    "emotion_average": {
        "map": """function (doc) {
                    emit(doc.c_location,doc.compound);
                  }""",
        "reduce": """function(keys, values) {
                    var sum = 0;
                    var num = 0;
                    for(var idx in values) {
                       sum = sum + values[idx];
                       num += 1;
                  }
                    var ave = sum/num
                    return ave;
        }"""
    }
}

db['_design/emotion_analyse'] = dict(language='javascript', views=views)
