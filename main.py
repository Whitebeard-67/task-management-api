from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import mysql.connector

def get_connection():
    try:
        return mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="project3"
        )
    
    except mysql.connector.Error as e:
        print(f"Database connection Failed: {e}")
        return None
app= FastAPI()

class Task(BaseModel):
    title: str

@app.get("/")
def home():
    return {"message": "Task Management API"}

tasks = [
    {"id": 1, "title": "Learn FastAPI"},
    {"id": 2, "title": "Build Project 3"},
]

@app.get("/tasks")
def get_tasks():
    db = get_connection()
    if db is None:
        raise HTTPException(
            status_code=500,
            detail="Database Connection Failed"
        )
    cursor = db.cursor()

    query = ("select * from tasks")   
    cursor.execute(query)
    results = cursor.fetchall()

    cursor.close()
    db.close()

    return results

@app.post("/tasks", status_code=201)
def create_task(task: Task):
    new_task= {
        "id": len(tasks)+1,
        "title": task.title
    }
    tasks.append(new_task)
    return new_task

@app.get("/tasks/search")
def search_task(title: str):
    results =[]

    for task in tasks:
        if title.lower() in task["title"].lower():
            results.append(task)

    return results
    
@app.get("/tasks/{task_id}")
def get_task(task_id: int):
    for task in tasks:
        if task["id"] == task_id:
            return task
        
    raise HTTPException(
        status_code=404,
        detail="Task Not Found"
    )   

@app.put("/tasks/{task_id}")
def update_task(task_id: int,task_data: Task):
    for task in tasks:
        if task["id"] == task_id:
            task["title"] = task_data.title
            return task
    raise HTTPException(
        status_code=404,
        detail="Task Doesn't Exist"
    )
@app.delete("/tasks/{task_id}")
def delete_task(task_id: int):
    for task in tasks:
        if task["id"] == task_id:
            tasks.remove(task)
            return "Task Removed"
    raise HTTPException(
        status_code=404,
        detail= "Task Not Found"
    )
