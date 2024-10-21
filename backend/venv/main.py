from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pymongo import MongoClient
from passlib.context import CryptContext
from pydantic import BaseModel
from models import User, UserInDB, collection, pwd_context

app = FastAPI()

# Configuración de CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Login(BaseModel):
    email: str
    password: str

@app.post("/register")
async def register(user: User):
    if not user.email or not user.password or not user.Utype:
        raise HTTPException(status_code=400, detail="Please fill in all fields.")

    existing_user = collection.find_one({"email": user.email})
    if existing_user:
        raise HTTPException(status_code=400, detail="User already exists.")

    hashed_password = pwd_context.hash(user.password)
    user_in_db = UserInDB(**user.dict(), hashed_password=hashed_password)
    
    result = collection.insert_one(user_in_db.dict())
    return {"message": "User registered successfully", "userId": str(result.inserted_id)}

@app.post("/login")
async def login(login_data: Login):
    user = collection.find_one({"email": login_data.email})
    if not user or not pwd_context.verify(login_data.password, user['hashed_password']):
        raise HTTPException(status_code=400, detail="Invalid email or password.")

    return {"message": "Login successful", "userId": str(user['_id'])}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)


class InputData(BaseModel):
    number: float

@app.post("/calculate-double/")
async def calculate_double(data: InputData):
    doubled_value = data.number * 5
    return {"doubled_value": doubled_value}

@app.post("/calculate-simple/")
async def calculate_simple(data: InputData):
    simple_value = data.number * 2
    return {"simple_value": simple_value}
