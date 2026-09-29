from fastapi import FastAPI, Depends
from auth import verify_token,oauth2_scheme
from routers import users,tasks
    
app= FastAPI()

app.include_router(users.router)
app.include_router(tasks.router)

@app.get("/protected")
def protected(token: str = Depends(oauth2_scheme)):
    payload = verify_token(token)

    return {
        "message": "you are authenticated",
        "user_id": payload["sub"]
    }

@app.get("/")
def home():
    return {"message": "Task Management API"}








    
 


