from index_feed import *
from whoosh.qparser import *
import operator

def news_searcher(ask):
    ix = index.open_dir(index_dir)
    news = dict()
    with ix.searcher() as searcher:
        query = MultifieldParser(["title", "body"], ix.schema, group=OrGroup).parse(ask.decode("utf-8"))
        results = searcher.search(query, limit=None)
        for r in results:
            news[r['title'], r['body'], r['link']] = r.score
    return sorted(news.items(), key=operator.itemgetter(1), reverse=True)


# CODIGO DE TESTE
#news = news_searcher("Portugal")
#for entry in news:
#	print "Score: " + str(entry[1])
#	print "Titulo: " + entry[0][0]
#	print "Descricao: " + entry[0][1]
#	print "Link: " + entry[0][2] + "\n"