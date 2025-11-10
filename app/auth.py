from fastapi import APIRouter, HTTPException
from app.database import users_collection
from app.utils import hash_password, verify_password, create_token

auth_router = APIRouter(prefix="/auth", tags=["Auth"])

@auth_router.post("/register")
def register_user(email: str, password: str, age: int):
    if users_collection.find_one({"email": email}):
        raise HTTPException(status_code=400, detail="Email already registered")
    
    hashed_pw = hash_password(password)
    users_collection.insert_one({"email": email, "password": hashed_pw, "age": age})
    return {"message": "User registered successfully"}

@auth_router.post("/login")
def login_user(email: str, password: str):
    user = users_collection.find_one({"email": email})
    if not user or not verify_password(password, user["password"]):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_token({"email": email, "age": user["age"]})
    return {"token": token, "email": email, "age": user["age"]}
