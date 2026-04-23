import pandas as pd
from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from typing import List, Optional
import random

df = pd.read_excel('questions_en.xlsx', header=0)
# print(df)
# print(df.head())
# print(df['subject'].unique())
# print(df['use'].unique())
# print(f"Missing values:\n{df.isnull().sum()}")
##############################################################################
#There are missing values in the "correct"-column. These lines will be dropped
###############################################################################
df_new = df.iloc[:68,:]
print(df_new)

class Question(BaseModel):
    question: str
    subject: str
    use: str
    correct: str
    answerA: str
    answerB: str
    answerC: str
    answerD: Optional[str] = None
    remark: Optional[str] = None

user_db = {
    "alice": "wonderland",
    "bob": "builder",
    "clementine": "mandarine",
    "admin": "4dm1N"
}
app = FastAPI(
    title="MCQ API",
    description="An API for MCQ with Authentification and admin-features"
    )

def parse_basic_auth(auth_header: Optional[str]) -> Optional[tuple]:
    """Parses the Basic Authentication header ('Basic username:password') and returns the username and password.
    """
    if not auth_header:
        return None
    try:
        auth_type, credentials = auth_header.split(" ", 1)
        if auth_type.lower() != 'basic':
            return None
        username, password = credentials.split(':', 1)
        return username, password
    except ValueError:
        return None
    
def authenticate_user(auth_header: Optional[str], require_admin: bool = False):
    """Authenticates the user based on the Basic Authentication header. If require_admin is True, also checks if the user is an admin.
    """
    credentials = parse_basic_auth(auth_header)
    if not credentials:
        raise HTTPException(status_code=401, detail="Authentication header missing or invalid")
    username, password = credentials
    expected = user_db.get(username)
    if expected is None or expected != password:
        raise HTTPException(status_code=401, detail="Invalid username or password")
    if require_admin and (username != "admin" or password != user_db["admin"]):
        raise HTTPException(status_code=403, detail="Admin privileges required")
    return username
    
#get question
#get health
#put question, admin
#docs
