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
DB_HOST = "localhost"
DB_PORT = "5433"
DB_NAME = os.getenv("POSTGRES_DB")

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
    with db_engine.connect() as conn:
        result = conn.execute(text("SELECT * FROM users WHERE id = :user_id"), {"user_id": user_id})
        result_list = result.fetchall()
        dict_result = {"id": result_list[0][0], "firstname": result_list[0][1], "lastname": result_list[0][2], "email": result_list[0][3], "password": result_list[0][4]}
        print(dict_result)
        return dict_result

if __name__ == "__main__":
    read_users_table(41)