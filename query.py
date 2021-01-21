import sqlite3 as sq3
from bottle import route, run, template, debug

@route('/query')
def query_db():
    #conn = sq3.connect('./ethblockchain.db')
    #c = conn.cursor()
    #c.execute()
    #c.close()
    return template('query')
    #return fetchall() # bottle expects a string or list of strings

# start web server
# go to http://localhost:8080/query
#add this at the very end:
debug(True) # XXX remove this eventually
run(reloader=True)
#run()
