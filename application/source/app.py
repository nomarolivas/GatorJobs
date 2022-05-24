import json
import os
from flask import request
from flask import Flask, render_template
from flask_mysqldb import MySQL

app = Flask(__name__)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'user'
app.config['MYSQL_PASSWORD'] = '123456'
app.config['MYSQL_DB'] = 'GatorJobsDB'

mysql = MySQL(app)

@app.route('/test', methods=['GET', 'POST'])
def test():
    if request.method == "POST":
        details = request.form
        skills = details['filter_by_skills']
        education = details['filter_by_Qualification']
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM Students")
        records = cur.fetchall()
        print(records)
        cur.close()
        return 'success'
    return render_template('index.jinja2')

@app.route('/filter')
def index():
    path = os.pardir + '/pages/Filter.html'
    return render_template(path)
