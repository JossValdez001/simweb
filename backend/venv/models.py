from pymongo import MongoClient
from passlib.context import CryptContext
from pydantic import BaseModel, EmailStr

# Configuración de MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client["simweb"]
collection = db["users"]

# Contexto para la encriptación de contraseñas
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class User(BaseModel):
    email: EmailStr
    password: str
    Utype: str

class UserInDB(User):
    hashed_password: str
