import mysql.connector
from config import DB_HOST,DB_NAME,DB_PASSWORD,DB_USER
from fastapi import HTTPException

def get_connection():
    try:
        return mysql.connector.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_NAME
        )

    except mysql.connector.Error as e:
        print(f"Database connection Failed: {e}")
        return None
    
def get_db():
    db= get_connection()

    if db is None:
        raise HTTPException(
            status_code=500,
            detail="Database Connection Failed"
            )
    try:
        yield db
    finally:
        db.close()