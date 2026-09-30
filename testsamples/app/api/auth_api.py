from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from app.core import security

router = APIRouter(prefix="/auth", tags=["Authentication Layer"])

@router.post("/token")
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):

    user = security.MOCK_USERS_DB.get(form_data.username)
    
    if not user or not security.verify_password(form_data.password, user["hashed_password"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password validation metrics.",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    token_expiry = timedelta(minutes=security.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = security.create_access_token(
        data={"sub": user["username"], "role": user["role"]}, 
        expires_delta=token_expiry
    )
    
    return {"access_token": access_token, "token_type": "bearer"}
