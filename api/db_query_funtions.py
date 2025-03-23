import os
from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, Boolean
from sqlalchemy.exc import ProgrammingError
from sqlalchemy.sql import text
from urllib.parse import quote_plus
from dotenv import load_dotenv

load_dotenv()

# Database connection details
DB_USER = quote_plus(os.getenv("POSTGRES_USER")) 
DB_PASSWORD = quote_plus(os.getenv("POSTGRES_PASSWORD"))
DB_HOST = quote_plus(os.getenv("DB_HOST")) # "postgres"
DB_PORT = quote_plus(os.getenv("DB_PORT")) #"5432" # "5432"
DB_NAME = quote_plus(os.getenv("POSTGRES_DB"))

# Create a connection string
connection_string = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/postgres"

# Connect to the PostgreSQL server
engine = create_engine(connection_string)
metadata = MetaData()

# function to read records from users table
def read_users_table(user_id: int):
    db_engine = create_engine(
        f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    )
    if user_id is None:
        with db_engine.connect() as conn:
            result = conn.execute(text("SELECT * FROM users"))
            result_list = result.fetchall()
            dict_result = [{"id": row[0], "firstname": row[1], "lastname": row[2], "email": row[3], "password": row[4]} for row in result_list]
            #print(dict_result)
            return dict_result
    else:
        with db_engine.connect() as conn:
            result = conn.execute(text("SELECT * FROM users WHERE id = :user_id"), {"user_id": user_id})
            result_list = result.fetchall()
            dict_result = {"id": result_list[0][0], "firstname": result_list[0][1], "lastname": result_list[0][2], "email": result_list[0][3], "password": result_list[0][4]}
            #print(dict_result)
            return dict_result

# function to insert records into users table    
def insert_users_table(firstname: str, lastname: str, email: str, password: str):
    db_engine = create_engine(
        f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    )
    with db_engine.begin() as conn:
        conn.execute(text("INSERT INTO users (firstname, lastname, email, password) VALUES (:firstname, :lastname, :email, :password)"), {"firstname": firstname, "lastname": lastname, "email": email, "password": password})
        print("Record inserted successfully")

# function to update records in users table
def update_users_table(user_id: int, firstname: str, lastname: str, email: str, password: str):
    db_engine = create_engine(
        f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    )
    with db_engine.begin() as conn:
        conn.execute(text("UPDATE users SET firstname = :firstname, lastname = :lastname, email = :email, password = :password WHERE id = :user_id"), {"user_id": user_id, "firstname": firstname, "lastname": lastname, "email": email, "password": password})
        print("Record updated successfully")

# function to delete records from users table
def delete_users_table(user_id: int):
    db_engine = create_engine(
        f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    )
    with db_engine.begin() as conn:
        conn.execute(text("DELETE FROM users WHERE id = :user_id"), {"user_id": user_id})
        print("Record deleted successfully")

if __name__ == "__main__":
    pass
    #delete_users_table(41)
    #read_users_table(41)
    #insert_users_table("John", "Doe", "demeveng@gmail.com", "test1234")
    #update_users_table(41, "John", "Doe", "demeveng@gmail3.com", "test1234")
