# db_config.py
import mysql.connector

def get_db_connection():
    return mysql.connector.connect(
        host="localhost",         # 🧘 Update if needed
        user="Babaji", 
        password="Mybabaji@143",  
        database="spiritual_db"
    )

