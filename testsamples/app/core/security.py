import hashlib
from datetime import datetime, timedelta, timezone
from typing import Optional
from jose import JWTError, jwt

# Cryptographic token signing configurations
JWT_SECRET_KEY = "70bc8db669fbb7c9dcf04ef051ef9b265d6c5df5e5ffae82d1c6df3d1c15f922"
JWT_ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode("utf-8")).hexdigest()

MOCK_USERS_DB = {
    "admin": {
        "username": "admin",
        "hashed_password": hash_password("AzureDemo2026!"),
        "role": "Administrator"
    },
    "network_engineer": {
        "username": "network_engineer",
        "hashed_password": hash_password("NetOpsPass2026!"),
        "role": "Engineer"
    }
}

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return hash_password(plain_password) == hashed_password

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + (expires_delta or timedelta(minutes=15))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, JWT_SECRET_KEY, algorithm=JWT_ALGORITHM)

def verify_access_token(token: str) -> Optional[dict]:
    try:
        payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=[JWT_ALGORITHM])
        username: str = payload.get("sub")
        if username and username in MOCK_USERS_DB:
            return MOCK_USERS_DB[username]
    except JWTError:
        pass
    return None
