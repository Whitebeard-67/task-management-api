from pwdlib import PasswordHash
from fastapi import HTTPException
from fastapi.security import OAuth2PasswordBearer
import jwt
from config import secretkey

password_hash = PasswordHash.recommended()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/users/login")

def create_access_token(user_id):
    payload = {
        "sub": str(user_id)
    }
    token= jwt.encode(payload, secretkey, algorithm="HS256")
    return token

def verify_token(token):
    try:
        return jwt.decode(token,secretkey,algorithms=["HS256"])
    except jwt.InvalidTokenError:
        raise HTTPException(
            status_code=401,
            detail="Invalid or expired token"
        )