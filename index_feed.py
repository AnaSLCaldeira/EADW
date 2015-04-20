import os

import feedparser
from whoosh import index
from whoosh.fields import *
from whoosh.index import create_in


source_dn_all = feedparser.parse("http://feeds.dn.pt/DN-Ultimas") # all news
source_jn_all = feedparser.parse("http://feeds.jn.pt/JN-ULTIMAS") # all news
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
    for feed in source_dn_all.entries:
        description = feed.summary.split("<img")
        title = feed.title.encode('utf-8')
        if checkIfDocExists(title, 'DN') is False:
            with open('dn_news.txt', 'a') as news_file:
                news_file.write(feed.title.encode('utf-8')+' \n')
            writer.add_document(title=feed.title, body=description[0], link=feed['feedburner_origlink'])

    for feed in source_jn_all.entries:
        description = feed.summary.split("<img")
        title = feed.title.encode('utf-8')
        if checkIfDocExists(title, 'JN') is False:
            with open('jn_news.txt', 'a') as news_file:
                news_file.write(feed.title.encode('utf-8')+' \n')
            writer.add_document(title=feed.title, body=description[0], link=feed['feedburner_origlink'])
    writer.commit()


def checkIfDocExists(title, feed):
    if feed == "DN":
        f = open('dn_news.txt', 'r')
    else:
        f = open('jn_news.txt', 'r')
    for line in f:
        if line.strip() == title:
            return True
    return False


#createIndex()
