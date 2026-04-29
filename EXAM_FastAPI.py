import pandas as pd
from fastapi import FastAPI, HTTPException, Depends, Header, Query, Response
from pydantic import BaseModel
from typing import List, Optional
import random

# data_file = 'questions_en.xlsx'
# df = pd.read_excel(data_file, header=0)
# print(df)
# print(df.head())
# print(df['subject'].unique())
# print(df['use'].unique())
# print(f"Missing values:\n{df.isnull().sum()}")
##############################################################################
#There are missing values in the "correct"-column. These lines will be dropped
###############################################################################
try:
    data_file = 'questions_en.xlsx'
    df = pd.read_excel(data_file, header=0) 
    df = df.replace({pd.NA: None, float('nan'): None})
    df_new = df.iloc[:68,:]
    df_new["id"] = range(1, len(df_new) + 1) #not asked but would be nice to have that for later checking the users' answers
    questions_store = df_new.to_dict(orient='records') #use dict for better handling in the API
except Exception as e:
    questions_store = []
    print(f"Error loading data: {e}")
#print(df_new)
#print(questions_store)

class PublicQuestion(BaseModel): #questions for user without the correct answer
    id: int
    question: str
    subject: str
    use: str
    responseA: str
    responseB: str
    responseC: Optional[str] = None
    responseD: Optional[str] = None
    remark: Optional[str] = None

class QuestionStore(PublicQuestion): #questions for the question store with the correct answer (admin only)
    correct: str
    
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
##############################################################
#Welcome page
##############################################################
@app.get("/", include_in_schema=False)
def welcome():
    return {"info": "MCQ API: use /questions, /health oder /docs für die Endpunkte."}
###############################################################
#define funtions for authentication
###############################################################
def parse_basic_auth(auth_header: Optional[str]) -> Optional[tuple]:
    """
    Parses the Basic Authentication header ('Basic username:password') and returns the username and password.
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
    """
    Authenticates the user based on the Basic Authentication header. If require_admin is True, also checks if the user is an admin.
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
##########################################################
#check if endpoint is working
##########################################################
@app.get("/health", 
        summary="Health Check", 
        description="Checks if the API is running and healthy."
        )
def health_check():
    """
    Checks if the API is running and healthy.
    """
    return {
        "status": "healthy"
        }
########################################################
#generate the questions
########################################################
@app.get("/questions", 
        summary="Generate Questions", 
        description=".",
        response_model=List[PublicQuestion]
        )
def generate_questions(
    use: str,
    subject: List[str] = Query(...),
    n: int = 5,
    authorization: Optional[str] = Header(None)
    ):
    """
    Generates either 5, 10, 15 or 20 questions from questions_store in random order.
    """
    authenticate_user(authorization)
    
    allowed_n = [5, 10, 15, 20]
    
    if n not in allowed_n:
        raise HTTPException(status_code=400, detail=f"Invalid number of questions. Allowed values are: {allowed_n}")
    
    filtered_questions = [q for q in questions_store if q['use'] == use and q['subject'] in subject]

    if len(filtered_questions) < n:
        raise HTTPException(
            status_code=400, 
            detail=f"Not enough questions available for the specified criteria. Requested: {n}, Available: {len(filtered_questions)}"
            )
    try:
        selected_questions = random.sample(filtered_questions, n)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    return selected_questions
############################################################
# Allow admin to add a new question to the questions_store
############################################################
@app.post("/questions", 
          summary="Add Question (Admin Only)", 
          description="Allows admin users to add a new question to the questions_store.",
          response_model=QuestionStore
          )  
def add_question(
    new_question: QuestionStore,
     response: Response,
    authorization: Optional[str] = Header(None),
    ):
    """
    Allows admin users to add a new question to the questions_store.
    """
    authenticate_user(authorization, require_admin=True) 
    
    questions_store.append(new_question.model_dump())
    
    response.headers["X-Status"] = "Question-Added-Successfully"

    return new_question
    
