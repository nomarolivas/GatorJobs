import mysql.connector
import json
import os
from flask import request
from flask import Flask, render_template
from flask import jsonify, url_for
from flask_mysqldb import MySQL
from mysql.connector import Error

# connecting to MySQL database
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


def insert_company_sign_up(Company_Name, Company_Email, Password, Description):
    query = "INSERT INTO Company(Company_Name, Company_Email, Password, Description)" \
            "VALUES(%s,%s,%s,%s,%s,%s,%s)"

    args = (Company_Name, Company_Email, Password, Description)

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
            if cursor.lastrowid:
                print('last insert id', cursor.lastrowid)
            else:
                print('last insert id not found')
    except Error as e:
        print("Error while connecting to MySQL", e)
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
            print("MySQL connection is closed")


def insert_company_sign_up(Username, Company_Email, Password, Description):
    query = "INSERT INTO Company(Username, Company_Email, Password, Description)" \
            "VALUES(%s,%s,%s,%s,%s,%s,%s)"

    args = (Username, Company_Email, Password, Description)

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
            if cursor.lastrowid:
                print('last insert id', cursor.lastrowid)
            else:
                print('last insert id not found')
    except Error as e:
        print("Error while connecting to MySQL", e)
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
            print("MySQL connection is closed")

def company_login(Username, Password):
    query = ("SELECT Username, Password FROM Company WHERE Company.Username = %s AND Company.Password = %s", [Username,
                                                                                                              Password])
    args = (Username, Password)

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
            if cursor.lastrowid:
                print('last get id', cursor.lastrowid)
            else:
                print('last get id not found')

            company = cursor.fetchall()

    except Error as e:
        print("Error while connecting to MySQL", e)
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
            print("MySQL connection is closed")

def company_homepage(Company_ID):
    query1 = ("SELECT Company_ID FROM Company WHERE Company.Company_ID = %s", [Company_ID])
    query2 = ("SELECT * FROM Jobs, Company WHERE Company.Company_ID = Jobs.Company_ID")
    args = (Company_ID)

    try:
        connection = mysql.connector.connect(host='34.102.11.81',
                                             database='GatorJobsDB',
                                             user='user',
                                             password='123456')
        if connection.is_connected():
            db_Info = connection.get_server_info()
            print("Connected to MySQL Server version ", db_Info)
            cursor = connection.cursor()
            #cursor.execute(query, args)
            if cursor.lastrowid:
                print('last get id', cursor.lastrowid)
            else:
                print('last get id not found')
    except Error as e:
        print("Error while connecting to MySQL", e)
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
            print("MySQL connection is closed")



def post_new_job(Title, Job_ID, Description, Annucal_compensation, Graduation_year_from, Graduation_year_to,
                 Required_skills, Category):
    query = "INSERT INTO Jobs(Title, Job_ID, Description, Annucal_compensation, Graduation_year_from, " \
            "Graduation_year_to, Required_skills, Category)" \
            "VALUES(%s,%s,%s,%s,%s,%s,%s)"

    args = (Title, Job_ID, Description, Annucal_compensation, Graduation_year_from, Graduation_year_to, Required_skills,
            Category)

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
            if cursor.lastrowid:
                print('last insert id', cursor.lastrowid)
            else:
                print('last insert id not found')
    except Error as e:
        print("Error while connecting to MySQL", e)
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
            print("MySQL connection is closed")


