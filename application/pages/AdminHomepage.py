import json
import mysql.connector
from mysql.connector import Error
from flask import request
from flask import Flask, render_template
from flask import jsonify, url_for
from flask_mysqldb import MySQL
app = Flask(__name__)
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'user'
app.config['MYSQL_PASSWORD'] = '123456'
app.config['MYSQL_DB'] = 'GatorJobsDB'
mysql = MySQL(app)
""" Admin Homepage:
POST
This will be a POST request that will retrieve all the student and company info. UI mockups in
M2 documentation (page 16).
Request json will contain the student id and company id.
Response will return all the student info and company info.
Get data from the Student and Company table. """


#connecting to MySQL database
def connect():

    try:
        connection = mysql.connector.connect(host='34.102.11.81',
                                         database='GatorJobsDB',
                                         user='user',
                                         password='123456')
        if connection.is_connected():
            db_Info = connection.get_server_info()
            print("Connected to MySQL Server version ", db_Info)
            cursor = connection.cursor()
            cursor.execute("select database();")
            record = cursor.fetchone()
            print("You're connected to database: ", record)

    except Error as e:
        print("Error while connecting to MySQL", e)
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
            print("MySQL connection is closed")

@app.route('/admin_homepage', methods=['GET'])
def admin_homepage(Student_ID, Company_ID):
    

    query1  = "SELECT * FROM Company INNER JOIN Jobs WHERE Company.Company_ID = Jobs.Company_ID"

    query2 = "SELECT * FROM Student"

    args = (Student_ID, Company_ID)

    try:
        connection = mysql.connector.connect(host='34.102.11.81',
                                         database='GatorJobsDB',
                                         user='user',
                                         password='123456')
        if connection.is_connected():
            db_Info = connection.get_server_info()
            print("Connected to MySQL Server version ", db_Info)
            cursor = connection.cursor()
            cursor.execute(query1, args)
            result1 = cursor.fetchall()
            cursor.execute(query2, args)
            result2 = cursor.fetchall()
            admin = cursor.fetchall()
            print(admin, result1, result2)
            # jobsDetails = json.dumps()
            jobsList = json.dumps(admin)
            cur.close()
            print("Access successful")
    except Error as e:
        print("Error while connecting to MySQL", e)
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
            print("MySQL connection is closed")
@app.route('/admin_homepage')
def index():
#    loadImages()
#    loadImage()
    return render_template('adminHome.html')