import os
from flask import Flask, render_template, request
from flask_mysqldb import MySQL

app = Flask(__name__)

app.config['MYSQL_HOST'] = os.environ['MYSQL_HOSTNAME']
app.config['MYSQL_USER'] = os.environ['MYSQL_USERNAME']
app.config['MYSQL_PASSWORD'] = os.environ['MYSQL_PASSWD']
app.config['MYSQL_DB'] = os.environ['MYSQL_DBNAME']

mysql = MySQL(app)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == "POST":
        details = request.form
        firstname = details['fname']
        cur = mysql.connection.cursor()
        cur.execute("SELECT last_name from datatable WHERE first_name = (%s)", (firstname,))
        allrecords = cur.fetchone()
        if allrecords:
          record = allrecords[0].encode("utf-8")
        else:
          record = ""
        mysql.connection.commit()
        cur.close()
        return render_template('index.html', data=record)
    else:
        return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0')
