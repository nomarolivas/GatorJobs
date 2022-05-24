from crypt import methods
import json
import datetime
import os
import logging
import uuid
from flask import Flask
from flask_bcrypt import Bcrypt
from unicodedata import category
import mysql.connector as sql_db
from mysql.connector import Error

logging.basicConfig(filename='/var/www/csc648-02-sp22-team05/application/pages/logs/logging.log', filemode='w',
                    format='%(name)s - %(levelname)s - %(message)s')
from flask import request
from flask import Flask, render_template, redirect
from flask import jsonify, url_for
from flask_mysqldb import MySQL
from InsertImage import loadImages
from RetrieveAndRevertImage import loadImage

app = Flask(__name__)
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'user'
app.config['MYSQL_PASSWORD'] = '123456'
app.config['MYSQL_DB'] = 'GatorJobsDB'
mysql = MySQL(app)
app = Flask(__name__)  # added this
bcrypt = Bcrypt(app)  # added this

db = sql_db.connect(host='localhost',
                    user='user',
                    passwd='123456',
                    db='GatorJobsDB',
                    port=3306)


@app.route('/results', methods=['POST', 'GET'])
def test():
    details = json.loads(request.get_json())
    print("Able to get request details")

    print(details)

    skills = details.get('filter_by_skills')

    print("Able to get skills")

    education = details.get('filter_by_Qualification')
    cur = mysql.connection.cursor()
    # if skills and eductaion is not set, return all details
    if not skills and not education:
        cur.execute("SELECT * FROM Student")
    elif not skills:
        # if only education is specified
        print("Looking for education")
        cur.execute(
            "SELECT * FROM Student, Student_Educational_Qualifications WHERE Student_Educational_Qualifications.Student_ID = Student.Student_ID AND Student_Educational_Qualifications.Degree = %s",
            [education])
    elif not education:
        # if only skills are mentioned
        print("Looking for skills")
        cur.execute("SELECT * FROM Student WHERE Student.Skills LIKE %s", ["%" + skills + "%"])
    else:
        # if both are mentioned
        print("Looking for skills and education")
        cur.execute(
            "SELECT * FROM Student, Student_Educational_Qualifications WHERE Student_Educational_Qualifications.Student_ID = Student.Student_ID AND Student_Educational_Qualifications.Degree = %s AND Student.Skills LIKE %s",
            [education, "%" + skills + "%"])
    students = cur.fetchall()
    print(students)
    studList = json.dumps(students)
    cur.close()
    print("Access successful")
    return render_template('results.html', students=studList)


@app.route('/filter')
def index():
    return render_template('Filter.html')


@app.route('/')
def default():
    return redirect(url_for('home'))


@app.route('/home')
def home():
    return render_template('homepage.html')


@app.route('/admin_login_route', methods=['GET', 'POST'])
def admin_login_route():
    return render_template('adminLogin.html')


@app.route('/admin_login', methods=['GET', 'POST'])
def admin_login():
    error = None
    if request.method == 'POST':
        params = json.loads(request.get_json())
        UserName = params.get('UserName')
        Password = params.get('Password')
        logging.warning("Able to get %s and %s", UserName, Password)
        logging.warning('Able to get username and password')

        query = "SELECT Username, Password FROM Admin WHERE Admin.Username = %s AND Admin.Password = %s"
        args = (UserName, Password)
        cursor = db.cursor(dictionary=True)
        cursor.execute(query, args)

        result = cursor.fetchall()
        username = result[0]['Username']
        password = result[0]['Password']
        isAuthenticated = False
        if username == UserName and password == Password:
            isAuthenticated = True
        cursor.close()

        if isAuthenticated:
            logging.warning(isAuthenticated)
            return redirect(url_for('adminHome'))
        else:
            error = "Username or Password is incorrect"
            return render_template('adminLogin.html', error=error)


@app.route('/adminHome', methods=['GET'])
def adminHome():
    return render_template('adminHome.html')


@app.route('/company_login_route', methods=['GET'])
def company_login_route():
    return render_template('companyLogin.html')


@app.route('/company_login_authenticate', methods=['POST'])
def company_login_authenticate():
    params = json.loads(request.get_json())
    compEmail = params.get("companyEmail")
    compPassword = params.get("companyPassword")
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT Email, Password, Company_ID FROM Company C WHERE C.Email = %s", [compEmail])

    result = cursor.fetchall()
    logging.warning("Printing result : ---------------> %s", result)
    logging.warning("Printing result[0] : ---------------> %s", result[0])
    compName = result[0]['Email']
    password = result[0]['Password']

    companyId = json.dumps(result)
    logging.warning("companyId -------->", companyId)

    PasswordDC = bcrypt.check_password_hash(password, compPassword)  # added this

    isAuthenticated = False
    if compName == compEmail and PasswordDC:
        isAuthenticated = True
    cursor.close()
    if isAuthenticated:
        return render_template('CompanyHomePage.html', companyId=companyId)
    else:
        error = "Username or Password is incorrect"
        return render_template('companyLogin.html', error=error)


@app.route('/CompanyHomePage', methods=['GET'])
def CompanyHomePage():
    return render_template('CompanyHomePage.html')


@app.route('/post_new_jobs', methods=['POST'])
def post_new_jobs():
    logging.warning("---------------------- Entered POST --------------------------")

    params = json.loads(request.get_json())
    job_title = params.get('InputJobTitle')
    job_desc = params.get('InputJobDescription')
    job_skills = params.get('InputSkills')
    job_domain = params.get('select_domain')
    job_salary = params.get('InputJobSalar')
    companyEmail = params.get('CompanyEmail')

    job_id = uuid.uuid4().int >> 64

    cur1 = db.cursor(dictionary=True)

    cur1.execute("SELECT C.Company_ID, C.Name, C.Description, C.Category, C.Name FROM Company C WHERE C.Email = %s",
                 [companyEmail])
    result1 = cur1.fetchall()
    companyId = result1[0]['Company_ID']
    cur1.close()
    logging.warning("Printing company ID ----------> %s", companyId)

    cursor = db.cursor(dictionary=True)
    try:
        cursor.execute(
            "INSERT INTO Jobs(`Job_ID`, `Title`, `Description`, `Annual_compensation`, `Required_skills`, `Category`, `Company_ID`) VALUES (%s, %s, %s, %s, %s, %s, %s)",
            [job_id, job_title, job_desc, job_salary, job_skills,
             job_domain, companyId])
        if cursor.lastrowid:
            logging.warning("Insert successful in jobs.")
        # else:
        #     logging.error("Error inserting into table student_jobs")
        db.commit()
        cursor.close()
    except mysql.connector.Error as err:
        logging.warning("Error -----------> %s", err)
        raise
    return render_template('CompanyHomePage.html')


@app.route('/companySignup', methods=['GET'])
def companySighup():
    return render_template('companySignup.html')


@app.route('/company_signup_method', methods=['POST'])
def company_signup_method():
    params = json.loads(request.get_json())
    compName = params.get('companyName')
    compEmail = params.get('companyEmail')
    compPass = params.get('companyPassword')
    compDesc = params.get('companyDescription')
    compCat = params.get('companyCategory')
    pw_hash = bcrypt.generate_password_hash(compPass)

    compID = str(uuid.uuid4())
    cur = db.cursor(dictionary=True)
    try:
        cur.execute(
            "INSERT INTO Company (`Company_ID`, `Username`, `Password`, `Name`, `Email`, `Description`, `Category`) VALUES (%s, %s, %s, %s, %s, %s, %s)",
            [compID, compEmail, pw_hash, compName, compEmail, compDesc, compCat])
        if cur.lastrowid:
            logging.warning("Insert successful in Company.")
            return render_template('companySignup.html')
        db.commit()
        cur.close()
    except Exception as err:
        logging.warning("Error -----------> %s", err)
        raise
    return render_template('CompanyHomePage.html', companyId=compID)


@app.route('/get_company_homepage', methods=['POST'])
def get_company_homepage():
    params = json.loads(request.get_json())
    companyEmail = params.get('companyEmail')

    cur1 = db.cursor(dictionary=True)

    cur1.execute("SELECT C.Company_ID, C.Name, C.Description, C.Category, C.Name FROM Company C WHERE C.Email = %s",
                 [companyEmail])
    result1 = cur1.fetchall()
    companyId = result1[0]['Company_ID']
    companyDetails = json.dumps(result1)
    cur1.close()

    logging.warning("Printing data :::::::: %s", result1)
    logging.warning("Printing data companyDetails :::::::: %s", companyDetails)

    cur2 = db.cursor(dictionary=True)

    cur2.execute(
        "SELECT J.Job_ID, J.Title, J.Description, J.Annual_compensation, J.Required_skills, J.Category FROM Jobs J JOIN Company C ON J.Company_ID = C.Company_ID WHERE C.Company_ID = %s",
        [companyId])
    result2 = cur2.fetchall()
    jobDetails = json.dumps(result2)
    cur2.close()

    logging.warning("Printing data for jobs :::::::: %s", result2)

    return render_template('CompanyHomePage.html', companyDetails=companyDetails, jobDetails=jobDetails)


# Routing to student login page
@app.route('/student_login_route', methods=['GET'])
def student_login_route():
    return render_template('studentLogin.html')


# Perform operations on student login page
@app.route('/student_authenticate', methods=['POST'])
def student_authenticate():
    # perform operations here
    params = json.loads(request.get_json())
    UserName = params.get('username')
    Password = params.get('password')
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT Student_ID, Password FROM Student S WHERE S.Student_ID = %s", [UserName])  # added this too

    result = cursor.fetchall()
    logging.warning("Printing result : ---------------> %s", result)
    logging.warning("Printing result[0] : ---------------> %s", result[0])
    username = result[0]['Student_ID']
    password = result[0]['Password']

    PasswordDC = bcrypt.check_password_hash(password, Password)  # added this

    isAuthenticated = False
    if username == UserName and PasswordDC:
        isAuthenticated = True
    cursor.close()
    if isAuthenticated:
        return render_template('studentHomepage.html')
    else:
        error = "Username or Password is incorrect"
        return render_template('studentLogin.html', error=error)


# Routing to student homepage
@app.route('/studentHomepage', methods=['GET'])
def studentHomepage():
    return render_template('studentHomepage.html')


# Routing to student sign up page
@app.route('/studentSignup', methods=['GET'])
def studentSignup():
    return render_template('studentSignup.html')


# This will store the sign up data in the student table
@app.route('/student_signup_method', methods=['POST'])
def student_signup_method():
    # perform operations here
    params = json.loads(request.get_json())
    Student_ID = params.get('studentId')
    Name = params.get('name')
    Phone_no = params.get('phoneNo')
    Date_of_birth = params.get('dob')
    Email = params.get('emailId')
    Password = params.get('password')
    Gender = params.get('gender')
    pw_hash = bcrypt.generate_password_hash(Password)  # added this

    logging.warning("Student_ID : --------> %s", Student_ID)
    logging.warning("Phone_no : --------> %s", Phone_no)

    cur = db.cursor(dictionary=True)
    try:
        cur.execute(
            "INSERT INTO Student (`Student_ID`, `Name`, `Phone_number`, `Date_of_birth`, `Email`, `Password`, `Gender`) VALUES (%s, %s, %s, %s, %s, %s, %s)",
            [Student_ID, Name, Phone_no, Date_of_birth, Email, pw_hash, Gender])
        if cur.lastrowid:
            logging.warning("Insert successful in Student.")
            return render_template('studentRegistrationTab.html')
        db.commit()
        cur.close()
    except Exception as err:
        logging.warning("Error -----------> %s", err)
        raise
    return render_template('studentSignup.html')


# Routing to student registration page
@app.route('/studentRegistrationTab', methods=['GET'])
def studentRegistrationTab():
    return render_template('studentRegistrationTab.html')


# Student registration and info storing
@app.route('/student_complete_registration', methods=['POST'])
def student_complete_registration():
    # perform operations here
    params = json.loads(request.get_json())
    # Students table
    studentId = params.get('student_id')
    fname = params.get('first_name')
    lname = params.get('last_name')
    name = fname + ' ' + lname
    address = params.get('address')
    dateOfBirth = params.get('date_of_birth')
    pincode = params.get('pincode')
    link = params.get('link')
    skills = params.get('skills')
    languages = params.get('languages')
    proficency = params.get('proficency')
    objective = params.get('objective')
    category = params.get('category')
    # profile picture BLOB
    # recommendation_letter_file BLOB

    # Student_Educational_Qualifications table
    degree = params.get('degree')
    gpa = params.get('GPA')
    qualificationDescription = params.get('qualification_description')
    educationStartDate = params.get('education_start_date')
    graduationYear = params.get('graduation_year')
    awards = params.get('awards')
    # degree certificate BLOB

    # Student_Certifications table
    certification = params.get('certification')
    awardingBody = params.get('awarding_body')
    certificationStartDate = params.get('certification_start_date')
    certificationEndDate = params.get('certification_end_date')
    certificationDescription = params.get('certification_description')
    # certificate_file BLOB

    # Student_Work_Experience table
    title = params.get('work_title')
    company = params.get('company')
    workStart_Date = params.get('work_start_date')
    workEndDate = params.get('work_end_date')
    position = params.get('position')
    workDescription = params.get('work_description')
    # experience_letter_file BLOB

    # save data into student 
    cur1 = db.cursor(dictionary=True)
    query1 = "UPDATE Student S SET S.Name = %s, S.Address = %s, S.Date_of_birth = %s, S.Pin_code = %s, S.Links = %s, S.Skills = %s, S.Languages_spoken = %s, S.Proficiency = %s, S.Objectives = %s, S.Category = %s WHERE S.Student_ID = %s"
    args1 = (name, address, dateOfBirth, pincode, link, skills, languages, proficency, objective, category, studentId)
    try:
        cur1.execute(query1, args1)
        if cur1.lastrowid:
            logging.warning("update successful in Student.")
        else:
            logging.error("Error inserting into table Student")
        db.commit()
        cur1.close()
    except mysql.connector.Error as err:
        logging.warning("Error -----------> %s", err)

    # save data into Student_Educational_Qualifications
    cur2 = db.cursor()
    query2 = "INSERT INTO Student_Educational_Qualifications (Student_ID, Degree, GPA, Start_date, Graduation_year, Description, Awards) VALUES (%s,%s,%s,%s,%s,%s,%s)"
    args2 = (studentId, degree, gpa, educationStartDate, graduationYear, qualificationDescription, awards)
    try:
        cur2.execute(query2, args2)
        if cur2.lastrowid:
            logging.warning("update successful in Student_Educational_Qualifications.")
        else:
            logging.error("Error inserting into table Student_Educational_Qualifications")
        db.commit()
        cur2.close()
    except mysql.connector.Error as err:
        logging.warning("Error -----------> %s", err)

    # save data into Student_Certifications
    cur3 = db.cursor()
    query3 = "INSERT INTO Student_Certifications (Student_ID, Certification, Awarding_body, Start_date, End_date, Description) VALUES (%s, %s, %s, %s, %s, %s)"
    args3 = (
    studentId, certification, awardingBody, certificationStartDate, certificationEndDate, certificationDescription)
    try:
        cur3.execute(query3, args3)
        if cur3.lastrowid:
            logging.warning("update successful in Student_Certifications.")
        else:
            logging.error("Error inserting into table Student_Certifications")
        db.commit()
        cur3.close()
    except mysql.connector.Error as err:
        logging.warning("Error -----------> %s", err)

    # save data into Student_Work_Experience
    cur4 = db.cursor()
    query4 = "INSERT INTO Student_Work_Experience (Student_ID, Title, Company_name, Position, Start_date, End_date, Description) VALUES (%s, %s, %s, %s, %s, %s, %s)"
    args4 = (studentId, title, company, position, workStart_Date, workEndDate, workDescription)
    try:
        cur4.execute(query4, args4)
        if cur4.lastrowid:
            logging.warning("update successful in Student_Work_Experience.")
        else:
            logging.error("Error inserting into table Student_Work_Experience")
        db.commit()
        cur4.close()
    except mysql.connector.Error as err:
        logging.warning("Error -----------> %s", err)

    return render_template('studentHomepage.html')


@app.route('/get_student_homepage_details', methods=['POST'])
def get_student_homepage_details():
    params = json.loads(request.get_json())
    # Students table
    studentId = params.get('studentId')

    # get data from student 
    cur1 = db.cursor(dictionary=True)
    cur1.execute(
        "SELECT S.Name, S.Address, S.Date_of_birth, S.Pin_code, S.Links, S.Skills, S.Languages_spoken, S.Proficiency, S.Objectives, S.Category FROM Student S WHERE S.Student_ID = %s",
        [studentId])
    result1 = cur1.fetchall()
    studentDetails = json.dumps(result1)
    cur1.close()

    # get data from Student_Educational_Qualifications
    cur2 = db.cursor(dictionary=True)
    cur2.execute(
        "SELECT E.Student_ID, E.Degree, E.GPA, E.Start_date, E.Graduation_year, E.Description, E.Awards FROM Student_Educational_Qualifications E WHERE E.Student_ID = %s",
        [studentId])
    result2 = cur2.fetchall()
    studentEducationDetails = json.dumps(result2, default=str)
    cur2.close()

    # get data from Student_Certifications
    cur3 = db.cursor(dictionary=True)
    cur3.execute(
        "SELECT C.Student_ID, C.Certification, C.Awarding_body, C.Start_date, C.End_date, C.Description FROM Student_Certifications C WHERE C.Student_ID = %s",
        [studentId])
    result3 = cur3.fetchall()
    studentCertificationDetails = json.dumps(result3, default=str)
    cur3.close()

    # get data from Student_Work_Experience
    cur4 = db.cursor(dictionary=True)
    cur4.execute(
        "SELECT W.Student_ID, W.Title, W.Company_name, W.Position, W.Start_date, W.End_date, W.Description FROM Student_Work_Experience W WHERE W.Student_ID = %s",
        [studentId])
    result4 = cur4.fetchall()
    studentExperienceDetails = json.dumps(result4, default=str)
    cur4.close()

    # get data from student_jobs
    cur5 = db.cursor(dictionary=True)
    cur5.execute(
        "SELECT S.Job_ID, S.Company_ID, C.Name, J.Title, J.Description FROM Student_Jobs S INNER JOIN Company C ON S.Company_ID = C.Company_ID INNER JOIN Jobs J ON S.Job_ID = J.Job_ID WHERE S.Student_ID = %s",
        [studentId])
    result5 = cur5.fetchall()
    studentAlertDetails = json.dumps(result5)
    cur5.close()

    return render_template('studentHomepage.html', studentDetails=studentDetails,
                           studentEducationDetails=studentEducationDetails,
                           studentCertificationDetails=studentCertificationDetails,
                           studentExperienceDetails=studentExperienceDetails, studentAlertDetails=studentAlertDetails)


# Admin matching students & jobs
@app.route('/match_method', methods=['GET'])
def match_method():
    # perform operations here
    return render_template('adminMatch.html')


# Routing to admin match
@app.route('/adminMatch', methods=['GET'])
def adminMatch():
    return render_template('adminMatch.html')


# Confirm and save data in student_jobs
@app.route('/match_student_jobs', methods=['POST'])
def match_student_jobs():
    params = json.loads(request.get_json())
    studentId = params.get('studentId')
    jobId = params.get('jobId')

    cursor1 = db.cursor(dictionary=True)
    cursor1.execute("SELECT Company_ID FROM Jobs J WHERE J.Job_ID = %s", [jobId])
    result1 = cursor1.fetchall()
    logging.warning("-------------- result: %s", result1)
    companyId = result1[0]['Company_ID']
    cursor1.close()

    cursor2 = db.cursor(dictionary=True)
    try:
        cursor2.execute("INSERT INTO `Student_Jobs` VALUES (%s, %s, %s)", [studentId, jobId, companyId])
        if cursor2.lastrowid:
            logging.warning("Insert successful in student_jobs.")
        else:
            logging.error("Error inserting into table student_jobs")
        db.commit()
        cursor2.close()
    except mysql.connector.Error as err:
        logging.warning("Error -----------> %s", err)
    return render_template('adminHome.html')


# Routing to admin jobs
@app.route('/adminJobs', methods=['GET'])
def adminJobs():
    return render_template('adminJobs.html')


# Routing to admin student
@app.route('/adminStudent', methods=['GET'])
def adminStudent():
    return render_template('adminStudent.html')


# Get student and job data for admin
@app.route('/get_data_for_admin', methods=['POST'])
def get_data_for_admin():
    db = sql_db.connect(host='localhost',
                        user='user',
                        passwd='123456',
                        db='GatorJobsDB',
                        port=3306)

    query1 = "SELECT S.Student_ID, Name, Objectives, Category, Degree, GPA FROM Student S JOIN Student_Educational_Qualifications Q ON S.Student_ID = Q.Student_ID"
    cursor1 = db.cursor(dictionary=True)
    # cursor1 = mysql.connection.cursor()
    cursor1.execute(query1)
    result1 = cursor1.fetchall()
    logging.warning("Printing student data: %s", result1)
    students = json.dumps(result1)
    cursor1.close()

    query2 = "SELECT J.Job_ID, C.Company_ID, J.Title, J.Description, J.Annual_compensation, J.Required_skills, J.Category, C.Name FROM Jobs J JOIN Company C ON J.Company_ID = C.Company_ID"
    cursor2 = db.cursor(dictionary=True)
    cursor2.execute(query2)
    result2 = cursor2.fetchall()
    logging.warning("Printing jobs data: %s", result2)
    jobs = json.dumps(result2)
    cursor2.close()

    return render_template("adminHome.html", studs=students, jbs=jobs)


@app.route('/filterStudentData', methods=['POST'])
def filterStudentData():
    params = json.loads(request.get_json())
    domain = params.get('domain')
    skill = params.get('skill')
    education = params.get('education')

    cur = db.cursor(dictionary=True)
    cur.execute(
        "SELECT S.Student_ID, Name, Objectives, Category, Degree, GPA FROM Student S JOIN Student_Educational_Qualifications Q ON S.Student_ID = Q.Student_ID WHERE S.Category = %s AND Q.Degree = %s AND S.Skills LIKE %s",
        [domain, education, "%" + skill + "%"])
    students = cur.fetchall()
    logging.warning("List of all students: %s", students)
    studList = json.dumps(students)
    cur.close()

    return render_template("adminHome.html", studList=studList)


@app.route('/filterJobData', methods=['POST'])
def filterJobData():
    params = json.loads(request.get_json())
    domain = params.get('domain')
    skill = params.get('skill')
    profile = params.get('profile')

    cur = db.cursor(dictionary=True)
    cur.execute(
        "SELECT J.Job_ID, C.Company_ID, Name, Description, Annual_compensation, Required_skills, J.Category FROM Jobs J JOIN Company C ON J.Company_ID = C.Company_ID WHERE J.Category = %s AND J.Required_skills LIKE %s AND J.Title = %s",
        [domain, "%" + skill + "%", profile])
    jobs = cur.fetchall()
    logging.warning("List of all jobs: %s", jobs)
    jobList = json.dumps(jobs)
    cur.close()

    return render_template("adminHome.html", jobList=jobList)


@app.route('/filterJobDataForStudents', methods=['POST'])
def filterJobDataForStudents():
    params = json.loads(request.get_json())
    domain = params.get('domain')
    skill = params.get('skill')
    profile = params.get('profile')

    logging.warn("Parameters -------------> : %s %s %s", domain, skill, profile)

    cur = db.cursor(dictionary=True)
    cur.execute(
        "SELECT J.Job_ID, C.Company_ID, Name, J.Description, Annual_compensation, Required_skills, J.Category FROM Jobs J JOIN Company C ON J.Company_ID = C.Company_ID WHERE J.Category = %s AND J.Required_skills LIKE %s AND J.Title = %s",
        [domain, "%" + skill + "%", profile])
    jobs = cur.fetchall()
    logging.warning("List of all jobs: %s", jobs)
    jobList = json.dumps(jobs)
    cur.close()

    return render_template("studentResult.html", jobList=jobList)


@app.route('/filterStudentDataForCompany', methods=['POST'])
def filterStudentDataForCompany():
    params = json.loads(request.get_json())
    domain = params.get('domain')
    skill = params.get('skill')
    education = params.get('profile')

    logging.warning("Parameters -------------> : %s %s %s", domain, skill, education)

    cur = db.cursor(dictionary=True)
    cur.execute(
        "SELECT S.Student_ID, Name, Objectives, Category, Degree, GPA FROM Student S JOIN Student_Educational_Qualifications Q ON S.Student_ID = Q.Student_ID WHERE S.Category = %s AND Q.Degree = %s AND S.Skills = %s",
        [domain, education, skill])
    students = cur.fetchall()
    logging.warning("List of all filtered students: %s", students)
    studentList = json.dumps(students)
    cur.close()

    return render_template("companySearchResult.html", studentList=studentList)


@app.route('/companySearchResult', methods=['GET'])
def companySearchResult():
    return render_template('companySearchResult.html')


# Routing to studentResult page
@app.route('/studentResult', methods=['GET'])
def studentResult():
    return render_template('studentResult.html')


# Routing to Jas' page
@app.route('/jas', methods=['GET'])
def jas():
    return render_template('jas.html')


# Routing to Risheek's page
@app.route('/risheek', methods=['GET'])
def risheek():
    return render_template('risheek.html')


# Routing to Purva's page
@app.route('/purva', methods=['GET'])
def purva():
    return render_template('purva.html')


# Routing to Shem's page
@app.route('/shem', methods=['GET'])
def shem():
    return render_template('shem.html')


# Routing to Nomar's page
@app.route('/nomar', methods=['GET'])
def nomar():
    return render_template('nomar.html')


# Routing to Yasin's page
@app.route('/yasin', methods=['GET'])
def yasin():
    return render_template('yasin.html')


# Routing to aboutUs page
@app.route('/aboutUs', methods=['GET'])
def aboutUs():
    return render_template('aboutUs.html')


@app.route('/get_student_by_id', methods=['POST'])
def get_student_by_id():
    params = json.loads(request.get_json())
    studentId = params.get('studentId')
    logging.warning("Fetching data for student : %s", studentId)

    cur = db.cursor(dictionary=True)
    cur.execute(
        "SELECT S.Student_ID, Name, Objectives, Category, Degree, GPA FROM Student S JOIN Student_Educational_Qualifications Q ON S.Student_ID = Q.Student_ID WHERE S.Student_ID = %s",
        [studentId])
    student = cur.fetchall()
    logging.warning("Student details: %s", student)
    studentDetails = json.dumps(student)
    cur.close()

    cur1 = db.cursor(dictionary=True)
    cur1.execute(
        "SELECT J.Job_ID, C.Company_ID, J.Title, J.Description, J.Annual_compensation, J.Required_skills, J.Category, C.Name FROM Jobs J JOIN Company C ON J.Company_ID = C.Company_ID")
    jobs = cur1.fetchall()
    logging.warning("Jobs:  %s", jobs)
    jobDetails = json.dumps(jobs)
    cur1.close()

    return render_template("adminStudent.html", students=studentDetails, job=jobDetails)


@app.route('/get_all_job_details', methods=['GET'])
def get_all_job_details():
    cur = db.cursor(dictionary=True)
    cur.execute(
        "SELECT J.Job_ID, C.Company_ID, J.Title, J.Description, J.Annual_compensation, J.Required_skills, J.Category, C.Name FROM Jobs J JOIN Company C ON J.Company_ID = C.Company_ID")
    jobs = cur.fetchall()
    logging.warning("Jobs:  %s", jobs)
    jobDetails = json.dumps(jobs)
    cur.close()

    return render_template("adminStudent.html", job=jobDetails)


@app.route('/get_job_by_id', methods=['POST'])
def get_job_by_id():
    params = json.loads(request.get_json())
    jobId = params.get('jobId')
    logging.warning("Fetching data for jobs : %s", jobId)

    cur = db.cursor(dictionary=True)
    cur.execute(
        "SELECT J.Job_ID, C.Company_ID, J.Title, J.Description, J.Annual_compensation, J.Required_skills, J.Category, C.Name FROM Jobs J JOIN Company C ON J.Company_ID = C.Company_ID AND J.Job_ID = %s",
        [jobId])
    jobs = cur.fetchall()
    logging.warning("Job details: %s", jobs)
    jobDetails = json.dumps(jobs)
    cur.close()

    cur1 = db.cursor(dictionary=True)
    cur1.execute(
        "SELECT S.Student_ID, Name, Objectives, Category, Degree, GPA FROM Student S JOIN Student_Educational_Qualifications Q ON S.Student_ID = Q.Student_ID")
    student = cur1.fetchall()
    logging.warning("Student:  %s", student)
    studentDetails = json.dumps(student)
    cur1.close()

    return render_template("adminJobs.html", job=jobDetails, stud=studentDetails)


@app.route('/get_all_student_details', methods=['GET'])
def get_all_student_details():
    cur = db.cursor(dictionary=True)
    cur.execute(
        "SELECT S.Student_ID, Name, Objectives, Category, Degree, GPA FROM Student S JOIN Student_Educational_Qualifications Q ON S.Student_ID = Q.Student_ID")
    student = cur.fetchall()
    logging.warning("Student:  %s", student)
    studentDetails = json.dumps(student)
    cur.close()

    return render_template("adminJobs.html", stud=studentDetails)


@app.route('/get_student_and_job_by_id', methods=['POST'])
def get_student_and_job_by_id():
    params = json.loads(request.get_json())
    jobId = params.get('jobId')
    studentId = params.get('studentId')

    cur = db.cursor(dictionary=True)
    cur.execute(
        "SELECT J.Job_ID, C.Company_ID, J.Title, J.Description, J.Annual_compensation, J.Required_skills, J.Category, C.Name FROM Jobs J JOIN Company C ON J.Company_ID = C.Company_ID AND J.Job_ID = %s",
        [jobId])
    jobs = cur.fetchall()
    logging.warning("Job details: %s", jobs)
    jobDetails = json.dumps(jobs)
    cur.close()

    cur1 = db.cursor(dictionary=True)
    cur1.execute(
        "SELECT S.Student_ID, Name, Objectives, Category, Degree, GPA FROM Student S JOIN Student_Educational_Qualifications Q ON S.Student_ID = Q.Student_ID WHERE S.Student_ID = %s",
        [studentId])
    student = cur1.fetchall()
    logging.warning("Student details: %s", student)
    studentDetails = json.dumps(student)
    cur1.close()

    return render_template("adminMatch.html", job=jobDetails, student=studentDetails)
