from fastapi import APIRouter,Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from auth.hashing import verify
from auth.auth_token import create_access_token
from datetime import timedelta

from app import models
from app.database import get_db

router = APIRouter(
    tags=["Login"],
    prefix="/login"
)

@router.post("/")
def login(request: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(models.Users).filter(models.Users.username == request.username).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid Credentials"
        )
    if not verify(request.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid Credentials"
        )
    access_token = create_access_token(
        data={"sub": user.username},
        expire_delta= timedelta(minutes=30)
    )
    return {
        "access_token": access_token,
         "token_type": "Bearer"
    }
