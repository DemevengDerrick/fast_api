from typing import Union
from fastapi import FastAPI
from pydantic import BaseModel
import db_query_funtions as dbq

app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/user/{user_id}")
def read_user(user_id: int):
    user = dbq.read_users_table(user_id)
    print(user)
    return user