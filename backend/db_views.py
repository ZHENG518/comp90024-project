import couchdb

db_ip = 'localhost'
db_name = 'twitter'
design_doc_name = 'basic_stats'


couch = couchdb.Server(f'http://admin:password@{db_ip}:5984')
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
