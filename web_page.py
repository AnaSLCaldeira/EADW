import web
from web import form

from relationships_discovery import *


render = web.template.render('templates/')

urls = ('/', 'index')
app = web.application(urls, globals())

myform = form.Form(
    form.Textbox("Search"),
    form.Textbox("Search with entities"),
    form.Textbox("Relationships with entity"))

class index: 
    def GET(self): 
        form = myform()
        return render.search_form(form)

    def POST(self): 
        form = myform() 
        if not form.validates(): 
            return render.search_form(form)
        else:
            # form.d.boe and form['boe'].value are equivalent ways of
            # extracting the validated arguments from the form.
            if form['Search'].value != "":
            	return get_news(form['Search'].value)
            elif form['Search with entities'].value != "":
            	return get_news_entities(form['Search with entities'].value)
            #elif form['Relationships with entity'].value != "":
            #	return relation_graph(form['Relationships with entity'].value)
            #elif form['Relationships with entity'].value != "":
            #	return get_relationships(form['Relationships with entity'].value)

if __name__=="__main__":
    web.internalerror = web.debugerror
    app.run()


#TRATAR CARACTERERES ESTRANHOS