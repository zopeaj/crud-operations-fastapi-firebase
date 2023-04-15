import uvicorn
import firebase_admin
import pyrebase
import json

from firebase_admin import credentials, auth
import firebase_admin
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.exceptions import HTTPException


cred = credentials.Certificate("hello-world-45396-firebase-adminsdk-5d4pr-6563300583.json")
firebase = firebase_admin.initialize_app(cred)
pb = pyrebase.initialize_app(json.load(open('firebase_config.json')))

app = FastAPI()
allow_all = ['*']
app.add_middleware(
    CORSMiddleware,
    allow_origins=allow_all,
    allow_credentials=True,
    allow_methods=allow_all,
    allow_headers=allow_all
)

@app.post("/signup", include_in_schema=False)
async def signup(request: Request):
   req = await request.json()
   email = req['email']
   password = req['password']
   if email is None or password is None:
       return HTTPException(detail={'message': 'Error! Missing Email or Password'}, status_code=400)
   try:
       user = auth.create_user(
           email=email,
           password=password
       )
       return JSONResponse(content={'message': f'Successfully created user {user.uid}'}, status_code=200)
   except:
       return HTTPException(detail={'message': 'Error Creating User'}, status_code=400)

@app.post("/login", include_in_schema=False)
async def login(request: Request):
   req_json = await request.json()
   email = req_json['email']
   password = req_json['password']
   try:
       user = pb.auth().sign_in_with_email_and_password(email, password)
       jwt = user['idToken']
       return JSONResponse(content={'token': jwt}, status_code=200)
   except:
       return HTTPException(detail={'message': 'There was an error logging in'}, status_code=400)

@app.post("/ping", include_in_schema=False)
async def validate(request: Request):
   headers = request.headers
   jwt = headers.get('authorization')
   print(f"jwt:{jwt}")
   user = auth.verify_id_token(jwt)
   return user["uid"]



## Signup endpoint

## Login endpoint

## ping endpoint

### FastAPI Signup Endpoint for Google Auth

# User ---> Email Password --- /signup -----> Email Password ---> Firebase auth

#                                     Success Status
#                                     UserID

# signup endpoint
# signup endpoint


### FastAPI Login Endpoint for Google Firebase Auth
# User ---> Email Password ---> /login -----> Email Password ------> Firebase auth

#                                         JWT Token

### Dummy Endpoint to Validate Firebase Authentication
# User -----> JWT Token in header ----> /ping -----> JWT Token --------> Firebase Auth
#                             Success

# ping endpoint




