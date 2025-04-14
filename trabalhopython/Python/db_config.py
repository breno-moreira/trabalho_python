import pymysql

DB_HOST = "127.0.0.1"
BD_USER = "root"
DB_PASSWORD = "root"
DB_NAME = "musica"

def connect_db():
    return pymysql.connect(
        host=DB_HOST,
        user=BD_USER,
        password=DB_PASSWORD,
        db=DB_NAME
    )