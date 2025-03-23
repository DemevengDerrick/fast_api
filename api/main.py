from typing import Union
from fastapi import FastAPI
from pydantic import BaseModel
import db_query_funtions as dbq

app = FastAPI()

class User(BaseModel):
    firstname: str
    lastname: str
    email: str
    password: str

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/user/")
def read_user(user_id: int = None):
    user = dbq.read_users_table(user_id)
    #print(user)
    return user

@app.post("/user/")
def create_user(user: User):
    dbq.insert_users_table(user.firstname, user.lastname, user.email, user.password)
    return user

@app.put("/user/{user_id}")
def update_user(user_id: int, user: User):
    dbq.update_users_table(user_id, user.firstname, user.lastname, user.email, user.password)
    return user

@app.delete("/user/{user_id}")
def delete_user(user_id: int):
    dbq.delete_users_table(user_id)
    return {f"message": "User {user_id} deleted successfully"}

if __name__ == "__main__":
    pass