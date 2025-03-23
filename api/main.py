from fastapi import FastAPI, Depends, HTTPException, status, APIRouter
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from pydantic import BaseModel
import db_query_funtions as dbq
from typing import Annotated
import secrets
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

security = HTTPBasic()

def get_current_username(credentials: HTTPBasicCredentials = Depends(security)):
    correct_username = secrets.compare_digest(credentials.username.encode("utf8"), os.getenv("POSTGRES_USER").encode("utf8"))
    correct_password = secrets.compare_digest(credentials.password.encode("utf8"), os.getenv("POSTGRES_PASSWORD").encode("utf8"))
    if not (correct_username and correct_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Basic"},
        )
    return credentials.username

auth_router = APIRouter(prefix="/auth", tags=["authenticated"], dependencies=[Depends(get_current_username)])

app.include_router(auth_router)

class User(BaseModel):
    firstname: str
    lastname: str
    email: str
    password: str

@app.get("/")
#@auth_router.get("/auth")
def read_current_user(username: Annotated[str, Depends(get_current_username)]):
    return {"Welcome ": username}

@app.get("/user/")
#@auth_router.get("/auth/user/")
def read_user(user_id: int = None):
    user = dbq.read_users_table(user_id)
    #print(user)
    return user

@app.post("/user/")
#@auth_router.post("/auth/user/")
def create_user(user: User):
    dbq.insert_users_table(user.firstname, user.lastname, user.email, user.password)
    return user

@app.put("/user/{user_id}")
#@auth_router.put("/auth/user/{user_id}")
def update_user(user_id: int, user: User):
    dbq.update_users_table(user_id, user.firstname, user.lastname, user.email, user.password)
    return user

@app.delete("/user/{user_id}")
#@auth_router.delete("/auth/user/{user_id}")
def delete_user(user_id: int):
    dbq.delete_users_table(user_id)
    return {f"message": "User {user_id} deleted successfully"}

if __name__ == "__main__":
    pass