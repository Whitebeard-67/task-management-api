from fastapi import APIRouter, HTTPException, Query, Depends
from pydantic import BaseModel, Field, field_validator
from database import get_db
from auth import verify_token,oauth2_scheme

router = APIRouter(prefix="/tasks", tags=["Tasks"])

class Task(BaseModel):
    title: str = Field(min_length=1, max_length=200)
    @field_validator("title")
    @classmethod
    def validate_title(cls, value):
        value=value.strip()
        if not value:
            raise ValueError("Title cannot be empty")
        return value

class TaskResponse(BaseModel):
    id: int
    title: str
    owner_id: int

@router.get("", response_model=list[TaskResponse])
def get_tasks(page: int = Query(1,ge=1), limit: int = Query(10,ge=1, le=100), sort: str ="id", order: str ="asc", db= Depends(get_db)):
    allowed_sort={
        "id": "id",
        "title": "title"
    }
    allowed_order = {
    "asc": "ASC",
    "desc": "DESC"
    }
    if sort not in allowed_sort:
        raise HTTPException(
            status_code=422,
            detail="Invalid Sort Field"
        )
    if order not in allowed_order:
        raise HTTPException(
            status_code=400,
            detail="Invalid Sort Order"
        )

    cursor = db.cursor(dictionary=True)

    offset = (page-1) * limit
    query = (f"select * from tasks order by {allowed_sort[sort]} {allowed_order[order]} limit %s offset %s")   
    cursor.execute(query,(limit,offset))
    results = cursor.fetchall()

    cursor.close()

    return results

@router.post("", status_code=201, response_model=TaskResponse )
def create_task(task: Task,token: str = Depends(oauth2_scheme),db=Depends(get_db)):
    cursor=db.cursor(dictionary=True)

    payload=verify_token(token)
    user_id = int(payload["sub"])

    query=("insert into tasks (title, owner_id) values(%s,%s)")

    cursor.execute(query,(task.title,user_id))
    db.commit()
    print("Task Added")

    task_id=cursor.lastrowid
    cursor.close()
    return {
        "id": task_id,
        "title": task.title,
        "owner_id": user_id    }

@router.get("/search", response_model=list[TaskResponse])
def search_task(title: str, db=Depends(get_db)):
    cursor=db.cursor(dictionary=True)
    query=("select * from tasks where title like %s")
    cursor.execute(query,(f"%{title}%",))

    results=cursor.fetchall()

    if not results :
        cursor.close()
        raise HTTPException(
        status_code=404,
        detail="Task Not Found")

    cursor.close()
    return results

@router.get("/{task_id}", response_model=TaskResponse)
def get_task(task_id: int, db= Depends(get_db)):
    cursor=db.cursor(dictionary=True)
    query=("select * from tasks where id=%s")
    cursor.execute(query,(task_id,))
    results=cursor.fetchone()

    if results is None:
        cursor.close()
        raise HTTPException(
        status_code=404,
        detail="Task Not Found")
    
    cursor.close()
    return results

@router.put("/{task_id}", response_model=TaskResponse)
def update_task(task_id: int,task_data: Task, token: str = Depends(oauth2_scheme),db=Depends(get_db)):
    cursor=db.cursor(dictionary=True)

    payload = verify_token(token)
    user_id = int(payload["sub"])
    query=("update tasks set title = %s where id=%s and owner_id=%s")
    cursor.execute(query,(task_data.title,task_id,user_id))
    db.commit()

    if cursor.rowcount == 0:
        cursor.close()
        raise HTTPException(
        status_code=404,
        detail="Task Doesn't Exist"
    )

    cursor.execute("select id, title, owner_id from tasks where id =%s",(task_id,))
    result= cursor.fetchone()

    cursor.close()

    return result

@router.delete("/{task_id}")
def delete_task(task_id: int, token: str= Depends(oauth2_scheme), db=Depends(get_db)):
    cursor=db.cursor(dictionary=True)

    payload=verify_token(token)
    user_id=payload["sub"]

    query=("delete from tasks where id =%s and owner_id=%s")
    cursor.execute(query,(task_id,user_id))
    db.commit()

    if cursor.rowcount == 0:
        cursor.close()
        
        raise HTTPException(
        status_code=404,
        detail= "Task Not Found"
    )

    cursor.close()
    return "Task Deleted"