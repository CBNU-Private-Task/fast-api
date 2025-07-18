from typing import List, Optional
from fastapi import APIRouter, Depends, status, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from pydantic import BaseModel, EmailStr
import datetime

from app.schemas.auth import CreateUser, UserLogin, UserOutput, LoginResponse, Token
from app.schemas.response import ApiResponse
from app.db.database import get_db
from app.utils.utils import hash_password, verify_password
from app.model.user import User
from app.core.Oauth import create_access_token

router = APIRouter()
    
# Get all Users
@router.get("/users", response_model=ApiResponse[List[UserOutput]], summary="Get All Users")
def get_users(db: Session = Depends(get_db)):
    users = db.query(User).all()
    print("Users is :",users)
    return {"data": users}

# Create User
@router.post("/reigster", status_code=status.HTTP_200_OK, response_model=ApiResponse[UserOutput], summary="Register User")
def register_user(user: CreateUser, db: Session = Depends(get_db)):
    
    hash_pass = hash_password(user.password)
    user.password = hash_pass
    
    new_user = User(**user.model_dump())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    return {"data": new_user, "message": "User have been registered successfully"}

@router.post("/token", response_model=Token)
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user_db = db.query(User).filter(User.email == form_data.username).first()
    if not user_db:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    if not verify_password(form_data.password, user_db.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token = create_access_token(data={"user_id": user_db.id})
    
    return {
        "access_token": access_token,
        "token_type": "bearer"
    }

# Login User (keep the original for other purposes)
@router.post("/login", response_model=LoginResponse)
def login_user(user: UserLogin, db: Session = Depends(get_db)):
    
    user_db = db.query(User).filter(User.email == user.email).first()
    if not user_db:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User does not exist")
    
    if not verify_password(user.password, user_db.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Password is incorrect")
    
    access_token = create_access_token(data={"user_id": user_db.id})
    
    return {
        "id": user_db.id,
        "email": user_db.email,
        "created_at": user_db.created_at,
        "access_token": access_token,
        "token_type": "bearer",
    }
    
    
# Delete User
@router.delete("/users/{user_id}", response_model=ApiResponse[None], summary="Remove User")
def delete_user(user_id: int, db: Session = Depends(get_db)):
    user_db = db.query(User).filter(User.id == user_id).first()
    if not user_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    
    db.delete(user_db)
    db.commit()
    
    return {"message": "User has been deleted successfully"}