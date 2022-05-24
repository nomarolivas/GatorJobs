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

@app.route('/student_homepage', methods=['GET'])

def student_homepage(Student_Id):

    
    #Requests Student infor that matches Student ID
    query1 = "SELECT * FROM Student WHERE Student.Student_ID= Student_Id"

    args = (Student_Id)
    #Requests Student Student Certifications that matches Student ID
    query2 = "SELECT * FROM Student_Certifications S  WHERE S.Student_ID= Student_Id"

    #Requests Student Student Educational Qualifications that matches Student ID
    query3 = "SELECT * FROM Student_Educational_Qualifications S WHERE S.Student_ID= Student_Id"

    #Requests Student Student Work Experience that matches Student ID
    query4 = "SELECT * FROM Student_Work_Experience S WHERE S.Student_ID= Student_Id"

    #connecting to MySQL database
    try:
        connection = mysql.connector.connect(host='34.102.11.81',
                                         database='GatorJobsDB',
                                         user='user',
                                         password='123456')
        if connection.is_connected():
            db_Info = connection.get_server_info()
            print("Connected to MySQL Server version ", db_Info)

            #Executes the 4 queries
            cursor = connection.cursor()
            cursor.execute(query1, args)
            cursor.execute(query2, args)
            cursor.execute(query3, args)
            cursor.execute(query4, args)
            
            #Requests Student Data from Student Table in MYSQL DB 
            student = cursor.fetchall()
            print(student)
            studList = json.dumps(students)
            cur.close()
            print("Acess successful")
    except Error as e:
        print("Error while connecting to MySQL", e)
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
            print("MySQL connection is closed")
            
@app.route('/student_homepage')
def index():
    return render_template('studentLogin.html')
            
