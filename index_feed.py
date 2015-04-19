import feedparser
import os
from whoosh import index


source_dn = feedparser.parse("http://feeds.dn.pt/DN-Portugal")
source_jn = feedparser.parse("http://feeds.jn.pt/JN-Pais")
index_dir = "indexdir"

def createIndex():
    if not os.path.exists(index_dir):
        os.mkdir(index_dir)

    if not index.exists_in(index_dir):
        schema = Schema(title=TEXT(stored=True), body=TEXT(stored=True), link=TEXT(stored=True))
        ix = create_in(index_dir, schema)
    else:
        ix = index.open_dir(index_dir)

    writer = ix.writer()
    for feed in source_dn.entries:
        description = feed.summary.split("<img")
        writer.add_document(title=feed.title, body=description[0], link=feed['feedburner_origlink'])
    for feed in source_jn.entries:
        description = feed.summary.split("<img")
        writer.add_document(title=feed.title, body=description[0], link=feed['feedburner_origlink'])
    writer.commit()

#createIndex()