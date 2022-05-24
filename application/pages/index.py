import json
from flask import request
from flask import Flask, render_template
from flask_mysqldb import MySQL

app = Flask(name)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'user'
app.config['MYSQL_PASSWORD'] = '123456'
app.config['MYSQL_DB'] = 'GatorJobsDB'

mysql = MySQL(app)

@app.route('/test', methods=['GET', 'POST'])
def index():
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
    return render_template('index.html')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/filter')
def index():
    return render_template('Filter.html')

@app.route('/test', methods=['POST'])
def test():
    output = request.get_json()
    print(output) # This is the output that was stored in the JSON within the browser
    print(type(output))
    result = json.loads(output) #this converts the json output to a python dictionary
    print(result) # Printing the new dictionary
    print(type(result))#this shows the json converted as a python dictionary
    return result
