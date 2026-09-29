from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import OAuth2PasswordRequestForm
from auth import password_hash, create_access_token
from database import get_db
from pydantic import BaseModel, Field
from mysql.connector import IntegrityError

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)

class Createuser(BaseModel):
    username: str = Field(min_length=4, max_length=50)
    password: str = Field(min_length=5)


@router.post("/register", status_code=201)
def user_reg(user: Createuser, db=Depends(get_db)):
    cursor=db.cursor()
    hashp=password_hash.hash(user.password)
    query=("insert into users (username,password_hash) values(%s,%s)")
    try:
        cursor.execute(query,(user.username,hashp))
        db.commit()

    except IntegrityError:
        raise HTTPException(
            status_code=409,
            detail="Username already exists"
        )
    finally: 
        cursor.close()
    return {"message": "User Registered Successfully"}

@router.post("/login" )
def userlogin(user: OAuth2PasswordRequestForm = Depends(),db=Depends(get_db)):
    cursor=db.cursor()
    cursor.execute("select id,password_hash from users where username=%s",(user.username,))
    hashp=cursor.fetchone()

    if hashp is None:
        cursor.close()
        raise HTTPException(
            status_code=401,
            detail="Invalid username or password"
        )
    userid= hashp[0]
    storedhash= hashp[1]
    if not password_hash.verify(user.password, storedhash):
        cursor.close()
        raise HTTPException(
            status_code=401,
            detail="Invalid username or password"
        )
    
    token= create_access_token(userid)
    cursor.close()
    return {"message": "login successful","access_token": token,"token_type": "bearer"}