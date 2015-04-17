import feedparser
from whoosh.index import create_in
from whoosh import index
from whoosh.fields import *
from whoosh.qparser import *
import os

source_dn = feedparser.parse("http://feeds.dn.pt/DN-Portugal")
source_jn = feedparser.parse("http://feeds.jn.pt/JN-Pais")
source_dn['feed']['title']
source_jn['feed']['title']

index_dir = "indexdir"


def createIndex():
    if not os.path.exists(index_dir):
        os.mkdir(index_dir)

    schema = Schema(title=TEXT(stored=True), body=TEXT(stored=True), link=TEXT(stored=True))

    if not index.exists_in(index_dir):
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

#dnFeeds(source_dn)
#jnFeeds(source_jn)


def news_searcher(ask):
    ix = index.open_dir(index_dir)
    doc_ordered = dict()
    array = []
    with ix.searcher() as searcher:
        query = MultifieldParser(["title", "body"], ix.schema, group=OrGroup).parse(ask.decode("utf-8"))
        results = searcher.search(query, limit=200)
        for i, r in enumerate(results):
            array.append((r['title'], r['body'], r['link']))
            doc_ordered[results.score(i)] = array[i]
    return doc_ordered

#createIndex()
