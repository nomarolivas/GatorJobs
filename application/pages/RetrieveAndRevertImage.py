import mysql.connector
import os.path
import base64


def write_file(data, filename):
    # Convert binary data to proper format and write it on Hard Disk

    while(not os.path.isfile(filename)):
        open(filename, 'x')
        print("created ", filename)

    with open(filename, 'wb') as file:
        print(filename)
        file.write(data)


def readBLOB(Student_ID, photo):
    print("Reading BLOB data from Student table")

    try:
        connection = mysql.connector.connect(host='34.102.11.81',
                                             database='GatorJobsDB',
                                             user='user',
                                             password='123456')

        cursor = connection.cursor()
        sql_fetch_blob_query = """SELECT * from Student where Student_ID = %s"""

        cursor.execute(sql_fetch_blob_query, (Student_ID,))
        record = cursor.fetchall()

        print(record)
        for row in record:
            print("Student_ID = ", row[0], )
            print("Username = ", row[1])
            print("Image = ", row[5])
            image = row[5]
            print("Storing Student image and bio-data on disk \n")
            write_file(image, photo)
            image.show()
            # write_file(file, bioData)

    except mysql.connector.Error as error:
        print("Failed to read BLOB data from MySQL table {}".format(error))

    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
            print("MySQL connection is closed")

def loadImage():
    readBLOB(6789, "/var/www/csc648-02-sp22-team05/application/photos/read/shem.png")
# readBLOB(2, "D:\Python\Articles\my_SQL\query_output\scott_photo.png",
#          "D:\Python\Articles\my_SQL\query_output\scott_bioData.txt")

