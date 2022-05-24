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


def convertToBinaryData(filename):
    with open(filename, 'rb') as file:
        binaryData = file.read()
    return binaryData


# Recieve student Info to store in Student Table when user registers as a Student
@app.route('/studentRegistrationTab', methods=['POST']) 
def insert_student_Registration(Student_ID, Name, Phone_number, Date_of_birth, Email, Password, Gender):
    

    query1 = "INSERT INTO Student(Student_ID, Name, Phone_number, Date_of_birth, Email, Password, Gender)" \
            "VALUES(%s,%s,%s,%s,%s,%s,%s)"


    query2 = "UPDATE Student SET Photo_path = %s, Address = %s, Phone_number= %s, Date_of_birth = %s, Pin_code = %s, Links = %s,  Skills = %s, Languages_spoken = %s, Proficiency = %s, Objectives = %s, Recommendation_letter = %s, Category = %s, Permissions = %s, Gender = %s WHERE Student.Student_ID = Student_ID, Student.Name = Name, Student.Phone_number = Phone_number, Student.Date_of_birth = Date_of_birth, Student.Email = Email, Student.Password = Password, Student.Gender = Gender"

        
    args = (Student_ID, Name, Phone_number, Date_of_birth, Email, Password, Gender)

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
            print(result1, result2)
            print("Acess successful")
    except Error as e:
        print("Error while connecting to MySQL", e)
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
            print("MySQL connection is closed")

@app.route('/studentRegistrationTab')
def index():
    return render_template('studentRegistrationTab.html')





