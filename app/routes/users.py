from fastapi import APIRouter, HTTPException
from app.models import User, UserLogin
from app.database import users_collection
from app.utils import hash_password, verify_password, create_token

router = APIRouter(prefix="/users", tags=["Users"])

@router.post("/register")
def register_user(user: User):
    existing = users_collection.find_one({"email": user.email})
    if existing:
        raise HTTPException(status_code=400, detail="User already exists")

    hashed_pw = hash_password(user.password)
    users_collection.insert_one({
        "email": user.email,
        "password": hashed_pw,
        "age": user.age
    })
    return {"message": "User registered successfully"}

@router.post("/login")
def login_user(user: UserLogin):
    db_user = users_collection.find_one({"email": user.email})
    if not db_user or not verify_password(user.password, db_user["password"]):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_token({"email": db_user["email"], "age": db_user["age"]})
    return {"token": token}
