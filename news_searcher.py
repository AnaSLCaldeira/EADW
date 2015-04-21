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
    

def get_news(ask):
  results = news_searcher(ask)
  news = ""
  for entry in results:
    news += "Score: " + str(entry[1]) + "\nTitulo: " + entry[0][0] + "\nDescricao: " + entry[0][1] + "\nLink: " + entry[0][2] + "\n\n"
  return news