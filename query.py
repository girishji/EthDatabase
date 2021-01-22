from bottle import route, run, template, request, debug
from ethdb import Database
import sqlite3 as sq3

@route('/query', method='GET')
def query_db():
    qstr = request.GET.qstring.strip()
    try: 
        db = Database()
        c = db.cursor()
        result = c.execute(qstr).fetchall()
        c.close()
        return template('query', rows=result)
    except sq3.OperationalError as er:
        return template('query', rows=[er])


# start web server
# go to http://localhost:8080/query
debug(True) # XXX remove this eventually
run(reloader=True)
#run()

# SQL
# PRAGMA table_info(table_name);
# SELECT txTo, count(txTo) FROM Tx GROUP BY txTo ORDER BY count(txTo) DESC LIMIT 5