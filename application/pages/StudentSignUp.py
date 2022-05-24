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


# Recieve student Info to store in Student Table when user signs up as a Student
@app.route('student_sign_up', methods=['POST'])
def student_sign_up(Student_ID, Name, Phone_number, Date_of_birth, Email, Password, Gender):
    
    #query to insert Student info into Student DB Table
    query = "INSERT INTO Student(Student_ID, Name, Phone_number, Date_of_birth, Email, Password, Gender)" \
            "VALUES(%s,%s,%s,%s,%s,%s,%s)"
        
    args = (Student_ID, Name, Phone_number, Date_of_birth, Email, Password, Gender)

    #connecting to MySQL database
    try:
        connection = mysql.connector.connect(host='34.102.11.81',
                                         database='GatorJobsDB',
                                         user='user',
                                         password='123456')
        if connection.is_connected():
            db_Info = connection.get_server_info()
            print("Connected to MySQL Server version ", db_Info)
            cursor = connection.cursor()
            cursor.execute(query, args)
            
    except Error as e:
        print("Error while connecting to MySQL", e)
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
            print("MySQL connection is closed")

@app.route('/student_sign_up')
def index():
    return render_template('studentSignup.html')
