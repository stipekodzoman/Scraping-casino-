import mysql.connector
from mysql.connector import errorcode
from dotenv import load_dotenv
import os
from time import sleep
load_dotenv()
def connect_db():
    try:
        connector = mysql.connector.connect(user=os.getenv("USER"),
                                    host=os.getenv("HOST"), database=os.getenv("DATABASE"))
        cursor = connector.cursor()
        query = '''CREATE TABLE IF NOT EXISTS RESULTS(
            id INT AUTO_INCREMENT PRIMARY KEY,
            value CHAR(1) not null,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )'''
        cursor.execute(query)
        return connector, cursor
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Something is wrong with your user name or password")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist")
        else:
            print(err)
        exit()
