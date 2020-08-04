import pymysql
from datetime import datetime

def search(nombre,lugar):
    name = nombre
    db = pymysql.connect(host='localhost', user='hanikua-hasi', passwd='', db='liidia')
    cursor = db.cursor()
    cursor.execute("SELECT * FROM pd WHERE Nombre = %s;", (name,))

    if cursor.fetchone():
        cursor.close()
        return 0
    else:
        insert_information(nombre, lugar)
        return 1


def insert_information(nombre,lugar):
    name, place = nombre, lugar
    fech = datetime.now()
    db = pymysql.connect(host='localhost', user='hanikua-hasi', passwd='', db='liidia')
    cursor = db.cursor()
    cursor.execute("INSERT INTO pd (id, Nombre, Fecha, Lugar) VALUES (%s, %s, %s, %s)", (0, name,fech,place))
    cursor.close()
    db.commit()
    return 1

