from flask import Flask
from flask import g
from flask import render_template
import sqlite3
import pkg_resources
import datetime

app = Flask(__name__,template_folder='templates')#, static_url_path="web/components/region/static"))

#db stuff.
def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(pkg_resources.resource_filename(__name__,"logs.db"))
    return db
@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()
#actual stuff.
@app.route('/add/<log_source>/<level>/<msg>')
def add(log_source,level,msg):
	db = get_db()
	c = db.cursor()
	c.execute("SELECT * FROM log_sources WHERE name='%s'"%log_source)
	rows = c.fetchall()
	if(len(rows) != 1):
		return "Error"
	id = rows[0][0]
	curr_date = str(datetime.datetime.now())
	c.execute("INSERT INTO logs VALUES (%d,'%s','%s','%s')"%(id,curr_date,level,msg))
	db.commit()
	return str(id) + curr_date + level + msg
		
@app.route('/display/<log_source>')
def display(log_source):
	db = get_db()
	c = db.cursor()
	c.execute("SELECT * FROM log_sources WHERE name='%s'"%log_source)
	rows = c.fetchall()
	if(len(rows) != 1):
		return default()
	id = rows[0][0]
	c.execute("SELECT * FROM logs WHERE source_id=%d"%id)
	rows = c.fetchall()
	return render_template('display.html', rows = rows, log_name=log_source)
@app.route('/')
def default():
	return render_template('display.html', rows = [], log_name="Such a log source does not exist...")
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=6000, debug=True)