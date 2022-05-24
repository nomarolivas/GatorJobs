import mysql.connector
import base64

def convertToBinaryData(filename):
#    img = Image.open(filename)

#    if filename.endswith(".jpg"):
#        filename = filename[:-4]
#        filename += ".png"

#    if filename.endswith(".jpeg"):
#        filename = filename[:-5]
#        filename += ".png"

#    img.save(filename)

    # Convert digital data to binary format
    with open(filename, 'rb') as file:
        binaryData = file.read()
    return binaryData


def insertBLOB(Student_ID, Username, Photo_path):
    print("Inserting BLOB into Student table")

    print(Student_ID, " ", Username, " ", Photo_path)
    try:
        connection = mysql.connector.connect(host='34.102.11.81',
                                             database='GatorJobsDB',
                                             user='user',
                                             password='123456')

        cursor = connection.cursor()
        sql_insert_blob_query = """ UPDATE Student SET Student.Photo_path = %s WHERE Student.Student_ID = %s; """

        studentPicture = convertToBinaryData(Photo_path)

        # Convert data into tuple format
        update_blob_tuple = (studentPicture, Student_ID)
        result = cursor.execute(sql_insert_blob_query, update_blob_tuple)
        connection.commit()
        print("Image and file inserted successfully as a BLOB into Student table", result)

    except mysql.connector.Error as error:
        print("Failed inserting BLOB data into MySQL table {}".format(error))

    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
            print("MySQL connection is closed")

def loadImages():
    insertBLOB(123, "Nomar", "/var/www/csc648-02-sp22-team05/application/photos/nomarOlivas.jpeg")
    insertBLOB(2020, "Jasneil", "/var/www/csc648-02-sp22-team05/application/photos/Jasneil.jpg")
    insertBLOB(4333, "Yasin", "/var/www/csc648-02-sp22-team05/application/photos/YasinHagos.jpeg")
    insertBLOB(456, "Risheek", "/var/www/csc648-02-sp22-team05/application/photos/risheekImg.jpg")
    insertBLOB(5050, "Purva", "/var/www/csc648-02-sp22-team05/application/photos/purva.jpg")
    insertBLOB(6789, "Shem", "/var/www/csc648-02-sp22-team05/application/photos/shem.jpg")

# Need path for where we store the about us pics
# insertBLOB(2, "Scott", "D:\Python\Articles\my_SQL\images\scott_photo.png")
