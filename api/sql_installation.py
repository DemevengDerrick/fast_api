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
DB_HOST = "localhost" # "postgres"
DB_PORT = "5433" # "5432"
DB_NAME = os.getenv("POSTGRES_DB")

# Create a connection string
connection_string = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/postgres"

# Connect to the PostgreSQL server
engine = create_engine(connection_string)
metadata = MetaData()

# Function to create the database if it doesn't exist
def create_database():
    with engine.connect() as conn:
        conn.execute(text("COMMIT"))  # Required to execute CREATE DATABASE
        result = conn.execute(
            text(f"SELECT 1 FROM pg_database WHERE datname = '{DB_NAME}'")
        )
        if not result.fetchone():
            conn.execute(text(f"CREATE DATABASE {DB_NAME}"))
            print(f"Database '{DB_NAME}' created.")
        else:
            print(f"Database '{DB_NAME}' already exists.")

# Function to create the users table
def create_users_table():
    # Connect to the specific database
    db_engine = create_engine(
        f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    )
    metadata.bind = db_engine

    users_table = Table(
        "users",
        metadata,
        Column("id", Integer, primary_key=True, autoincrement=True),
        Column("firstname", String, nullable=False),
        Column("lastname", String, nullable=False),
        Column("email", String, nullable=False, unique=True),
        Column("password", String, nullable=False),
    )

    try:
        metadata.create_all(db_engine)
        print("Table 'users' created or already exists.")
    except ProgrammingError as e:
        print(f"Error creating table: {e}")

    return users_table

# Function to populate the users table with fictitious data
def populate_users_table(users_table):
    db_engine = create_engine(
        f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    )
    with db_engine.begin() as conn:
        # Check if the table is empty
        result = conn.execute(text("SELECT COUNT(*) FROM users"))
        count = result.scalar()
        if count == 0:
            # Insert 10 fictitious records
            fictitious_users = [
                {"firstname": "John", "lastname": "Doe", "email": "john.doe@example.com", "password": "password123"},
                {"firstname": "Jane", "lastname": "Smith", "email": "jane.smith@example.com", "password": "password123"},
                {"firstname": "Alice", "lastname": "Johnson", "email": "alice.johnson@example.com", "password": "password123"},
                {"firstname": "Bob", "lastname": "Brown", "email": "bob.brown@example.com", "password": "password123"},
                {"firstname": "Charlie", "lastname": "Davis", "email": "charlie.davis@example.com", "password": "password123"},
                {"firstname": "Diana", "lastname": "Miller", "email": "diana.miller@example.com", "password": "password123"},
                {"firstname": "Eve", "lastname": "Wilson", "email": "eve.wilson@example.com", "password": "password123"},
                {"firstname": "Frank", "lastname": "Moore", "email": "frank.moore@example.com", "password": "password123"},
                {"firstname": "Grace", "lastname": "Taylor", "email": "grace.taylor@example.com", "password": "password123"},
                {"firstname": "Hank", "lastname": "Anderson", "email": "hank.anderson@example.com", "password": "password123"},
            ]
            conn.execute(users_table.insert(), fictitious_users)
            print("Inserted 10 fictitious records into 'users' table.")
        else:
            print("'users' table already populated.")

# Main execution
if __name__ == "__main__":
    create_database()
    users_table = create_users_table()
    print(users_table)
    populate_users_table(users_table)