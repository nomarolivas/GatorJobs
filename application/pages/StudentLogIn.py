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


@app.route('/student_login', methods=['POST'])


def student_login(UserName, Password):
    
    #Checks if username and password is stored in SQL DB
    query = "SELECT Username, Password FROM Student WHERE Student.Username = %s AND Student.Password = %s"
        
    args = (UserName, Password)

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
            result1 = cursor.fetchall()
            print(result1)
            # studList = json.dumps(students)
            print("Acess successful")
    except Error as e:
        print("Error while connecting to MySQL", e)
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
            print("MySQL connection is closed")

@app.route('/student_login')
def index():
    return render_template('studentSignup.html')
